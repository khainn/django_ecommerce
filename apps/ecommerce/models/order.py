from django.db import models

from common.models import BaseModel
from apps.ecommerce.common.enums import OrderStatus
from apps.ecommerce.models.cart import Cart


class Order(BaseModel):
    """Order model"""
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    total_price = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.value) for status in OrderStatus],
        default=OrderStatus.PENDING.value
    )
    
    # Foreign keys
    cart = models.OneToOneField(
        Cart,
        on_delete=models.CASCADE,
        related_name="order"
    )
    
    class Meta(BaseModel.Meta):
        db_table = "ecommerce_orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
    
    def __str__(self):
        return f"Order {self.id} - {self.customer_name} - {self.status}" 