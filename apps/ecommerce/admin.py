from django.contrib import admin
from django.contrib.admin import register, AdminSite
from django.conf import settings

from apps.ecommerce.models import (
    ProductCategory, 
    Product, 
    Cart, 
    CartItem, 
    Order
)
from apps.ecommerce.utils.admin import set_admin_site_url

# Create a custom admin site that doesn't include auth models
class EcommerceAdminSite(AdminSite):
    site_header = 'E-commerce Administration'
    site_title = 'E-commerce Admin'
    index_title = 'E-commerce Admin Portal'
    
    # Customize the "View site" URL
    def each_context(self, request):
        context = super().each_context(request)
        # Set the site_url (View site link)
        context['site_url'] = getattr(settings, 'ADMIN_SITE_URL', '/ecommerce/')
        return context

# Initialize the custom admin site
ecommerce_admin = EcommerceAdminSite(name='ecommerce_admin')

# Register models with the custom admin site
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity_in_stock', 'total_sold', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
    inlines = [CartItemInline]

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'customer_address')
    readonly_fields = ('cart', 'total_price', 'created_at')

# Register models with the custom admin site
ecommerce_admin.register(ProductCategory, ProductCategoryAdmin)
ecommerce_admin.register(Product, ProductAdmin)
ecommerce_admin.register(Cart, CartAdmin)
ecommerce_admin.register(Order, OrderAdmin)

# Also register with the default admin for convenience if needed
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)

# Set the site_url for all admin sites
set_admin_site_url(getattr(settings, 'ADMIN_SITE_URL', '/ecommerce/'))
