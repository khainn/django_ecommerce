from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.ecommerce.common.enums import OrderStatus
from apps.ecommerce.models.cart import Cart
from common.models import BaseModel


class Order(BaseModel):
    """Order model"""
    customer_name = models.CharField(max_length=100, verbose_name=_("Customer Name"))
    customer_phone = models.CharField(max_length=20, verbose_name=_("Customer Phone"))
    customer_email = models.EmailField(max_length=100, blank=True, null=True, verbose_name=_("Customer Email"))
    customer_address = models.CharField(verbose_name=_("Customer Address"))
    notes = models.TextField(blank=True, default="", verbose_name=_("Notes"))
    total_price = models.IntegerField(verbose_name=_("Total Price"))
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.value) for status in OrderStatus],
        default=OrderStatus.PENDING.value,
        verbose_name=_("Status")
    )

    # Foreign keys
    cart = models.OneToOneField(
        Cart,
        on_delete=models.CASCADE,
        related_name="order",
        verbose_name=_("Cart")
    )

    class Meta(BaseModel.Meta):
        db_table = "ecommerce_orders"
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order {self.id} - {self.customer_name} - {self.status}"
