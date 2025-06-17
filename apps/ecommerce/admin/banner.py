from django import forms

from apps.ecommerce.models import Banner
from apps.ecommerce.widgets import NoCurrentFileClearableFileInput
from .common import BaseModelAdmin


class BannerAdminForm(forms.ModelForm):
    """Custom form for Banner admin."""
    
    class Meta:
        model = Banner
        fields = "__all__"
        widgets = {
            'image': NoCurrentFileClearableFileInput,
            'title': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'}),
            'target_url': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
            'position': forms.NumberInput(attrs={'min': 0, 'step': 1}),
        }


class BannerAdmin(BaseModelAdmin):
    """Admin configuration for Banner model."""
    
    list_display = ("short_id", "title", "position", "is_active", "created_at")
    list_filter = ("is_active", "position", "created_at")
    search_fields = ("title", "target_url")
    readonly_fields = ("image_preview",)
    fields = ("title", "image_preview", "image", "target_url", "position", "is_active")
    list_editable = ("position", "is_active")
    form = BannerAdminForm
    ordering = ("position", "-created_at")

    def get_queryset(self, request):
        """Order banners by position and creation date."""
        return super().get_queryset(request).order_by('position', '-created_at')
