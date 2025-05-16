import uuid

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
        super().save(*args, **kwargs)

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
