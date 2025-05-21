import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from cloudinary_storage.storage import MediaCloudinaryStorage

from common.models import BaseModel


def validate_image_size(image):
    """Validate image size is less than 2MB"""
    if image.size > 2 * 1024 * 1024:  # 2MB
        raise ValidationError("Image size must be less than 2MB")


def product_image_path(instance, filename):
    """Generate file path for product image with slugified name"""
    ext = filename.split(".")[-1]
    slug_name = slugify(instance.name)
    unique_id = str(uuid.uuid4())[:8]
    return f"products/{slug_name}-{unique_id}.{ext}"


class ProductCategory(BaseModel):
    """Product category model"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")

    class Meta(BaseModel.Meta):
        db_table = "ecommerce_product_categories"
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name


class Product(BaseModel):
    """Product model"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    price = models.IntegerField()
    quantity_in_stock = models.IntegerField()
    image = models.ImageField(
        upload_to=product_image_path,
        blank=True,
        null=True,
        validators=[validate_image_size],
        storage=MediaCloudinaryStorage()
    )
    total_sold = models.IntegerField(default=0)
    excerpt = models.TextField(blank=True, default="")
    content = models.TextField(blank=True, default="")

    # Foreign keys
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True
    )

    class Meta(BaseModel.Meta):
        db_table = "ecommerce_products"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
