from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.ecommerce.models.product import Product
from common.models import BaseModel


class Cart(BaseModel):
    """Shopping cart model"""
    # BaseModel already provides id, created_at, and updated_at fields

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta(BaseModel.Meta):
        db_table = "ecommerce_carts"
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(BaseModel):
    """Shopping cart item model"""
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))

    # Foreign keys
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Cart")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name=_("Product")
    )

    class Meta(BaseModel.Meta):
        db_table = "ecommerce_cart_items"
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart {self.cart.id}"
