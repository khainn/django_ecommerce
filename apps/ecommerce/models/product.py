from django.db import models

from common.models import BaseModel


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
    image_url = models.CharField(max_length=255, blank=True, default="")
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