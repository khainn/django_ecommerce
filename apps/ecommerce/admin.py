from django.conf import settings
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django import forms
from django.urls import path, include

from apps.ecommerce.models import Blog, BlogImage, Cart, CartItem, Order, Product, ProductCategory, Banner
from apps.ecommerce.utils.admin import set_admin_site_url
from apps.ecommerce.widgets import NoCurrentFileClearableFileInput


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
        # Add language switching URL
        context["i18n_urls"] = True
        return context

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('i18n/', include('django.conf.urls.i18n')),
        ]
        return custom_urls + urls

# Initialize the custom admin site
ecommerce_admin = EcommerceAdminSite(name="ecommerce_admin")

# Register models with the custom admin site
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at",)

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            'image': NoCurrentFileClearableFileInput,
        }

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "quantity_in_stock", "total_sold", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("image_preview",)
    fields = ("name", "description", "price", "quantity_in_stock", "category",
              "image_preview", "image", "excerpt", "content")
    form = ProductAdminForm

    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="300" style="border:1px solid #ccc; padding:5px; border-radius:8px;" />',)
        return _("No image")

    image_preview.short_description = _("Image Preview")

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    inlines = [CartItemInline]

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "customer_email", "status", "total_price", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "customer_phone", "customer_email", "customer_address", "notes")
    readonly_fields = ("cart", "total_price", "created_at")

class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    fields = ("image", "image_preview", "caption", "display_order")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="300" style="border:1px solid #ccc; padding:5px; border-radius:8px;" />',)
        return _("No image")

    image_preview.short_description = _("Image Preview")

class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
        widgets = {
            'image': NoCurrentFileClearableFileInput,
        }

class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "date", "created_at")
    list_filter = ("date", "created_at")
    search_fields = ("title", "excerpt", "content")
    readonly_fields = ("image_preview",)
    fields = ("title", "author", "date", "image_preview", "image", "excerpt", "content")
    prepopulated_fields = {"title": ("title",)}
    inlines = [BlogImageInline]
    form = BlogAdminForm

    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="300" style="border:1px solid #ccc; padding:5px; border-radius:8px;" />',)
        return _("No image")

    image_preview.short_description = _("Image Preview")

class BlogImageAdminForm(forms.ModelForm):
    class Meta:
        model = BlogImage
        fields = "__all__"
        widgets = {
            'image': NoCurrentFileClearableFileInput,
        }

class BlogImageAdmin(admin.ModelAdmin):
    list_display = ("id", "blog", "caption", "display_order", "created_at")
    list_filter = ("blog", "created_at")
    search_fields = ("blog__title", "caption")
    readonly_fields = ("image_preview",)
    fields = ("blog", "image_preview", "image", "caption", "display_order")
    form = BlogImageAdminForm

    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="300" style="border:1px solid #ccc; padding:5px; border-radius:8px;" />',)
        return _("No image")

    image_preview.short_description = _("Image Preview")

class BannerAdminForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"
        widgets = {
            'image': NoCurrentFileClearableFileInput,
        }

class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "position", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "target_url")
    readonly_fields = ("image_preview",)
    fields = ("title", "image_preview", "image", "target_url", "position", "is_active")
    list_editable = ("position", "is_active")
    form = BannerAdminForm

    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="300" style="border:1px solid #ccc; padding:5px; border-radius:8px;" />',)
        return _("No image")

    image_preview.short_description = _("Image Preview")

# Register models with the custom admin site
ecommerce_admin.register(ProductCategory, ProductCategoryAdmin)
ecommerce_admin.register(Product, ProductAdmin)
ecommerce_admin.register(Cart, CartAdmin)
ecommerce_admin.register(Order, OrderAdmin)
ecommerce_admin.register(Blog, BlogAdmin)
ecommerce_admin.register(BlogImage, BlogImageAdmin)
ecommerce_admin.register(Banner, BannerAdmin)

# Also register with the default admin for convenience if needed
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogImage, BlogImageAdmin)
admin.site.register(Banner, BannerAdmin)

# Set the site_url for all admin sites
set_admin_site_url(getattr(settings, "ADMIN_SITE_URL", "/ecommerce/"))
