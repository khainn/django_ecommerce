from django.conf import settings
from django.contrib import admin
from django.contrib.admin import AdminSite

from apps.ecommerce.models import Blog, BlogImage, Cart, CartItem, Order, Product, ProductCategory
from apps.ecommerce.utils.admin import set_admin_site_url


# Create a custom admin site that doesn't include auth models
class EcommerceAdminSite(AdminSite):
    site_header = "E-commerce Administration"
    site_title = "E-commerce Admin"
    index_title = "E-commerce Admin Portal"

    # Customize the "View site" URL
    def each_context(self, request):
        context = super().each_context(request)
        # Set the site_url (View site link)
        context["site_url"] = getattr(settings, "ADMIN_SITE_URL", "/ecommerce/")
        return context

# Initialize the custom admin site
ecommerce_admin = EcommerceAdminSite(name="ecommerce_admin")

# Register models with the custom admin site
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at",)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "quantity_in_stock", "total_sold", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("image_preview",)
    fields = ("name", "description", "price", "quantity_in_stock", "category",
              "image", "image_preview", "excerpt", "content")

    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            return f'<img src="{obj.image.url}" width="150" />'
        return "No image"

    image_preview.short_description = "Image Preview"
    image_preview.allow_tags = True

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    inlines = [CartItemInline]

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "status", "total_price", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "customer_phone", "customer_address")
    readonly_fields = ("cart", "total_price", "created_at")

class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    fields = ("image", "image_preview", "caption", "display_order")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            return f'<img src="{obj.image.url}" width="150" />'
        return "No image"

    image_preview.short_description = "Image Preview"
    image_preview.allow_tags = True

class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "author", "date", "created_at")
    list_filter = ("date", "created_at")
    search_fields = ("title", "excerpt", "content")
    readonly_fields = ("image_preview",)
    fields = ("title", "slug", "author", "date", "image", "image_preview", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [BlogImageInline]

    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            return f'<img src="{obj.image.url}" width="150" />'
        return "No image"

    image_preview.short_description = "Image Preview"
    image_preview.allow_tags = True

class BlogImageAdmin(admin.ModelAdmin):
    list_display = ("id", "blog", "caption", "display_order", "created_at")
    list_filter = ("blog", "created_at")
    search_fields = ("blog__title", "caption")
    readonly_fields = ("image_preview",)
    fields = ("blog", "image", "image_preview", "caption", "display_order")

    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            return f'<img src="{obj.image.url}" width="150" />'
        return "No image"

    image_preview.short_description = "Image Preview"
    image_preview.allow_tags = True

# Register models with the custom admin site
ecommerce_admin.register(ProductCategory, ProductCategoryAdmin)
ecommerce_admin.register(Product, ProductAdmin)
ecommerce_admin.register(Cart, CartAdmin)
ecommerce_admin.register(Order, OrderAdmin)
ecommerce_admin.register(Blog, BlogAdmin)
ecommerce_admin.register(BlogImage, BlogImageAdmin)

# Also register with the default admin for convenience if needed
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogImage, BlogImageAdmin)

# Set the site_url for all admin sites
set_admin_site_url(getattr(settings, "ADMIN_SITE_URL", "/ecommerce/"))
