from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import escape

from apps.ecommerce.models import Order
from .common import BaseModelAdmin, CART_TABLE_STYLES


class OrderAdmin(BaseModelAdmin):
    list_display = ("short_id", "customer_name", "customer_email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "customer_phone", "customer_email", "customer_address", "notes")
    readonly_fields = ("customer_name", "customer_phone", "customer_email", "customer_address", 
                      "notes", "cart_items_display", "created_at")
    exclude = ("cart", "total_price")
    list_per_page = 30
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'cart__items__product', 'cart__items__product__category'
        )
    
    def total_price_display(self, obj):
        return f"{obj.total_price:,} ₫" if obj.total_price else "0 ₫"
    
    total_price_display.short_description = _("Total Price")
    total_price_display.admin_order_field = 'total_price'
    
    def cart_items_display(self, obj):
        if not obj.cart or not obj.cart.items.exists():
            return _("No items in cart")
        
        html_parts = [
            f'<table style="{CART_TABLE_STYLES["table"]}">',
            '<thead>',
            '<tr>',
            f'<th style="{CART_TABLE_STYLES["header"]} min-width: 200px;">{escape(_("Product"))}</th>',
            f'<th style="{CART_TABLE_STYLES["header"]} width: 80px; text-align: center;">{escape(_("Quantity"))}</th>',
            f'<th style="{CART_TABLE_STYLES["header"]} width: 120px; text-align: right;">{escape(_("Unit Price"))}</th>',
            f'<th style="{CART_TABLE_STYLES["header"]} width: 130px; text-align: right;">{escape(_("Total"))}</th>',
            '</tr>',
            '</thead>',
            '<tbody>'
        ]
        
        for item in obj.cart.items.all():
            unit_price = item.product.price
            line_total = unit_price * item.quantity
            
            # Format currency (VND) and escape strings for security
            unit_price_formatted = f"{unit_price:,} ₫"
            line_total_formatted = f"{line_total:,} ₫"
            product_name = escape(item.product.name)
            
            html_parts.extend([
                '<tr>',
                f'<td style="{CART_TABLE_STYLES["cell"]}">{product_name}</td>',
                f'<td style="{CART_TABLE_STYLES["cell_center"]}">{item.quantity}</td>',
                f'<td style="{CART_TABLE_STYLES["cell_right"]}">{unit_price_formatted}</td>',
                f'<td style="{CART_TABLE_STYLES["cell_right"]} font-weight: 600;">{line_total_formatted}</td>',
                '</tr>'
            ])
        
        # Add total row
        total_formatted = f"{obj.total_price:,} ₫"
        html_parts.extend([
            f'<tr style="{CART_TABLE_STYLES["total_row"]}">',
            f'<td style="{CART_TABLE_STYLES["cell"]}" colspan="3">{escape(_("Total Price"))}</td>',
            f'<td style="{CART_TABLE_STYLES["total_cell"]}">{total_formatted}</td>',
            '</tr>',
            '</tbody>',
            '</table>'
        ])
        
        return mark_safe(''.join(html_parts))
    
    cart_items_display.short_description = _("Cart Items")
