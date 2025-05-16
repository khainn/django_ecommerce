import uuid
import os

from django.db import models
from django.utils.text import slugify

from common.models import BaseModel


def blog_image_path(instance, filename):
    """Generate file path for blog image with slugified title"""
    ext = filename.split(".")[-1]
    slug_title = slugify(instance.blog.title if hasattr(instance, "blog") else instance.title)
    unique_id = str(uuid.uuid4())[:8]
    return f"blogs/{slug_title}-{unique_id}.{ext}"


class Blog(BaseModel):
    """Blog model"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.CharField(max_length=100, default="Admin")
    date = models.DateField()
    image = models.ImageField(upload_to=blog_image_path, blank=True, null=True)
    excerpt = models.TextField(blank=True, default="")
    content = models.TextField(blank=True, default="")
    
    class Meta(BaseModel.Meta):
        db_table = "ecommerce_blogs"
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
            
        # Check if this is an existing blog with an image being changed
        if self.pk:
            try:
                old_instance = Blog.objects.get(pk=self.pk)
                if old_instance.image and self.image != old_instance.image:
                    # Delete the old image file
                    if os.path.isfile(old_instance.image.path):
                        os.remove(old_instance.image.path)
            except (Blog.DoesNotExist, ValueError, FileNotFoundError):
                pass  # Handle case where old image doesn't exist or can't be found
                
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        # Delete the image file when the blog is deleted
        if self.image:
            try:
                if os.path.isfile(self.image.path):
                    os.remove(self.image.path)
            except (ValueError, FileNotFoundError):
                pass  # Handle case where image doesn't exist or can't be found
        
        super().delete(*args, **kwargs)
        
    @property
    def all_images(self):
        """Get all images for this blog including the main image and gallery images"""
        images = []
        if hasattr(self, "gallery"):
            images.extend([img.image for img in self.gallery.all()])
        return images


class BlogImage(BaseModel):
    """Blog image model for gallery images"""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to=blog_image_path)
    caption = models.CharField(max_length=200, blank=True, default="")
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta(BaseModel.Meta):
        db_table = "ecommerce_blog_images"
        verbose_name = "Blog Image"
        verbose_name_plural = "Blog Images"
        ordering = ["display_order"]

    def __str__(self):
        return f"Image for {self.blog.title}"
        
    def save(self, *args, **kwargs):
        # Check if this is an existing blog image with an image being changed
        if self.pk:
            try:
                old_instance = BlogImage.objects.get(pk=self.pk)
                if old_instance.image and self.image != old_instance.image:
                    # Delete the old image file
                    if os.path.isfile(old_instance.image.path):
                        os.remove(old_instance.image.path)
            except (BlogImage.DoesNotExist, ValueError, FileNotFoundError):
                pass  # Handle case where old image doesn't exist or can't be found
                
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Delete the image file when the blog image is deleted
        if self.image:
            try:
                if os.path.isfile(self.image.path):
                    os.remove(self.image.path)
            except (ValueError, FileNotFoundError):
                pass  # Handle case where image doesn't exist or can't be found
        
        super().delete(*args, **kwargs)
