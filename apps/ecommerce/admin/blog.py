"""
Blog and BlogImage admin configurations.
"""

from django import forms
from django.contrib import admin

from apps.ecommerce.models import Blog, BlogImage
from apps.ecommerce.widgets import NoCurrentFileClearableFileInput
from .common import BaseModelAdmin, ImagePreviewMixin


class BlogImageInline(admin.TabularInline, ImagePreviewMixin):
    """Inline admin for BlogImage model."""
    
    model = BlogImage
    extra = 1
    fields = ("image", "image_preview", "caption", "display_order")
    readonly_fields = ("image_preview",)
    classes = ('collapse',)


class BlogAdminForm(forms.ModelForm):
    """Custom form for Blog admin."""
    
    class Meta:
        model = Blog
        fields = "__all__"
        widgets = {
            'image': NoCurrentFileClearableFileInput,
            'title': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'}),
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }


class BlogAdmin(BaseModelAdmin):
    """Admin configuration for Blog model."""
    
    list_display = ("short_id", "title", "author", "date", "created_at")
    list_filter = ("date", "created_at")
    search_fields = ("title", "excerpt", "content", "author")
    readonly_fields = ("image_preview",)
    fields = ("title", "author", "date", "image_preview", "image", "excerpt", "content")
    inlines = [BlogImageInline]
    form = BlogAdminForm
    date_hierarchy = 'date'
    list_per_page = 15

    def get_queryset(self, request):
        """Optimize queryset with prefetch_related for blog images."""
        return super().get_queryset(request).prefetch_related('blogimage_set')


class BlogImageAdminForm(forms.ModelForm):
    """Custom form for BlogImage admin."""
    
    class Meta:
        model = BlogImage
        fields = "__all__"
        widgets = {
            'image': NoCurrentFileClearableFileInput,
        }


class BlogImageAdmin(BaseModelAdmin):
    """Admin configuration for BlogImage model."""
    
    list_display = ("short_id", "blog", "caption", "display_order", "created_at")
    list_filter = ("blog", "created_at")
    search_fields = ("blog__title", "caption")
    readonly_fields = ("image_preview",)
    fields = ("blog", "image_preview", "image", "caption", "display_order")
    form = BlogImageAdminForm
    list_select_related = ("blog",)

    def get_queryset(self, request):
        """Optimize queryset with select_related for blog."""
        return super().get_queryset(request).select_related('blog')
