from .common import ecommerce_admin
from .product import ProductCategoryAdmin, ProductAdmin
from .order import OrderAdmin
from .blog import BlogAdmin, BlogImageAdmin
from .banner import BannerAdmin

# Import models
from apps.ecommerce.models import Blog, BlogImage, Order, Product, ProductCategory, Banner

# Register models with the custom admin site
ecommerce_admin.register(ProductCategory, ProductCategoryAdmin)
ecommerce_admin.register(Product, ProductAdmin)
ecommerce_admin.register(Order, OrderAdmin)
ecommerce_admin.register(Blog, BlogAdmin)
ecommerce_admin.register(BlogImage, BlogImageAdmin)
ecommerce_admin.register(Banner, BannerAdmin)

# Also register with the default admin for convenience if needed
from django.contrib import admin
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogImage, BlogImageAdmin)
admin.site.register(Banner, BannerAdmin)

# Set the site_url for all admin sites
from django.conf import settings
from apps.ecommerce.utils.admin import set_admin_site_url
set_admin_site_url(getattr(settings, "ADMIN_SITE_URL", "/ecommerce/"))

__all__ = [
    'ecommerce_admin',
    'ProductCategoryAdmin',
    'ProductAdmin', 
    'OrderAdmin',
    'BlogAdmin',
    'BlogImageAdmin',
    'BannerAdmin',
]
