import uuid
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
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
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    image = models.ImageField(
        upload_to=banner_image_path,
        storage=MediaCloudinaryStorage(),
        verbose_name=_("Image")
    )
    target_url = models.URLField(max_length=255, blank=True, null=True, verbose_name=_("Target URL"))
    position = models.PositiveIntegerField(default=0, verbose_name=_("Position"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta(BaseModel.Meta):
        db_table = "ecommerce_banners"
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")
        ordering = ["position", "-created_at"]

    def __str__(self):
        return self.title 
