import uuid
from django.db import models
from django.utils.text import slugify
from cloudinary_storage.storage import MediaCloudinaryStorage

from common.models import BaseModel


def banner_image_path(instance, filename):
    """Generate file path for banner image"""
    ext = filename.split(".")[-1]
    slug_title = slugify(instance.title)
    unique_id = str(uuid.uuid4())[:8]
    return f"banners/{slug_title}-{unique_id}.{ext}"


class Banner(BaseModel):
    """Banner model for homepage and other pages"""
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to=banner_image_path,
        storage=MediaCloudinaryStorage()
    )
    target_url = models.URLField(blank=True, default="")
    position = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        db_table = "ecommerce_banners"
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ["position", "-created_at"]

    def __str__(self):
        return self.title 