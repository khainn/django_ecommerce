import uuid
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from cloudinary_storage.storage import MediaCloudinaryStorage

from common.models import BaseModel


def blog_image_path(instance, filename):
    """Generate file path for blog image with slugified title"""
    ext = filename.split(".")[-1]
    slug_title = slugify(instance.blog.title if hasattr(instance, "blog") else instance.title)
    unique_id = str(uuid.uuid4())[:8]
    return f"blogs/{slug_title}-{unique_id}.{ext}"


class Blog(BaseModel):
    """Blog model"""
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    author = models.CharField(max_length=100, default="Admin", verbose_name=_("Author"))
    date = models.DateField(verbose_name=_("Date"))
    image = models.ImageField(
        upload_to=blog_image_path,
        blank=True,
        null=True,
        storage=MediaCloudinaryStorage(),
        verbose_name=_("Image")
    )
    excerpt = models.TextField(blank=True, default="", verbose_name=_("Excerpt"))
    content = models.TextField(blank=True, default="", verbose_name=_("Content"))

    class Meta(BaseModel.Meta):
        db_table = "ecommerce_blogs"
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
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
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="gallery", verbose_name=_("Blog"))
    image = models.ImageField(
        upload_to=blog_image_path,
        storage=MediaCloudinaryStorage(),
        verbose_name=_("Image")
    )
    caption = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Caption"))
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta(BaseModel.Meta):
        db_table = "ecommerce_blog_images"
        verbose_name = _("Blog Image")
        verbose_name_plural = _("Blog Images")
        ordering = ["display_order"]

    def __str__(self):
        return f"Image for {self.blog.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
