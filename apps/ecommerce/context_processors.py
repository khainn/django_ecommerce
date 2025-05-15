"""Custom context processors for the ecommerce app."""
from django.conf import settings


def admin_site_url(request):
    """Add the admin site URL to the template context."""
    return {
        'admin_site_url': getattr(settings, 'ADMIN_SITE_URL', '/ecommerce/'),
        'admin_view_site_text': getattr(settings, 'ADMIN_VIEW_SITE_TEXT', 'E-commerce Store')
    } 