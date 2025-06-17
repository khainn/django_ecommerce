"""
Common admin configurations, mixins, and custom admin site.
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.urls import path, include


# Constants for better maintainability
ADMIN_IMAGE_PREVIEW_STYLE = (
    "border:1px solid #ccc; padding:5px; border-radius:8px; "
    "max-height:200px; object-fit:cover;"
)

CART_TABLE_STYLES = {
    'table': (
        'border-collapse: collapse; width: auto; max-width: 800px; '
        'margin-top: 10px; min-width: 600px; font-family: Arial, sans-serif;'
    ),
    'header': (
        'background-color: #f8f9fa; border: 1px solid #dee2e6; '
        'padding: 12px; text-align: left; font-weight: 600;'
    ),
    'cell': 'border: 1px solid #dee2e6; padding: 12px;',
    'cell_center': 'border: 1px solid #dee2e6; padding: 12px; text-align: center;',
    'cell_right': 'border: 1px solid #dee2e6; padding: 12px; text-align: right;',
    'total_row': 'background-color: #f8f9fa; font-weight: 600;',
    'total_cell': (
        'border: 1px solid #dee2e6; padding: 12px; text-align: right; '
        'color: #28a745; font-weight: 600;'
    )
}


class EcommerceAdminSite(AdminSite):
    """Custom admin site that doesn't include auth models."""
    
    site_header = "E-commerce Administration"
    site_title = "E-commerce Admin"
    index_title = "E-commerce Admin Portal"

    def each_context(self, request):
        context = super().each_context(request)
        context["site_url"] = getattr(settings, "ADMIN_SITE_URL", "/ecommerce/")
        context["i18n_urls"] = True
        context["available_languages"] = settings.LANGUAGES
        context["current_language"] = request.LANGUAGE_CODE
        return context

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('i18n/', include('django.conf.urls.i18n')),
        ]
        return custom_urls + urls


# Initialize the custom admin site
ecommerce_admin = EcommerceAdminSite(name="ecommerce_admin")


class ShortUUIDMixin:
    def short_id(self, obj):
        return str(obj.id)[:8] if obj.id else "-"
    
    short_id.short_description = _("ID")
    short_id.admin_order_field = 'id'


class ImagePreviewMixin:
    """Mixin to provide image preview functionality for admin classes."""
    
    def image_preview(self, obj):
        """Display image preview in admin with improved styling and security."""
        if obj.image:
            image_url = escape(obj.image.url)
            return mark_safe(
                f'<img src="{image_url}" width="300" style="{ADMIN_IMAGE_PREVIEW_STYLE}" />'
            )
        return _("No image")

    image_preview.short_description = _("Image Preview")


class BaseModelAdmin(admin.ModelAdmin, ImagePreviewMixin, ShortUUIDMixin):
    """Base admin class with common configurations."""
    list_per_page = 25
    show_full_result_count = False
