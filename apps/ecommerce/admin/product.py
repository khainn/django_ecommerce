"""
Product and ProductCategory admin configurations.
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from apps.ecommerce.models import Product, ProductCategory
from apps.ecommerce.widgets import NoCurrentFileClearableFileInput
from .common import BaseModelAdmin


class ProductCategoryAdmin(BaseModelAdmin):
    list_display = ("short_id", "name", "description", "created_at", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")
    ordering = ("name",)
    
    def get_queryset(self, request):
        return super().get_queryset(request)


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            'image': NoCurrentFileClearableFileInput,
            'name': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
            'content': forms.Textarea(attrs={'rows': 8, 'cols': 80}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
            'phone_number': forms.TextInput(attrs={'placeholder': '0123456789'}),
        }


class ProductAdmin(BaseModelAdmin):
    """Admin configuration for Product model."""
    
    list_display = ("short_id", "name", "price", "quantity_in_stock", "total_sold", "category", "phone_number", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("name", "description", "phone_number")
    readonly_fields = ("image_preview", "total_sold")
    fields = ("name", "description", "price", "quantity_in_stock", "category",
              "image_preview", "image", "excerpt", "content", "phone_number")
    form = ProductAdminForm
    list_select_related = ("category",)
    list_per_page = 20

    def get_queryset(self, request):
        """Optimize queryset with select_related for better performance."""
        return super().get_queryset(request).select_related('category')
