"""Admin utilities."""
from django.contrib import admin
from django.conf import settings


def set_admin_site_url(url=None):
    """
    Set the 'View site' URL for all admin sites.
    
    Args:
        url (str, optional): The URL to set. If None, uses ADMIN_SITE_URL from settings.
    """
    if url is None:
        # Use the ADMIN_SITE_URL from settings, or default to '/'
        url = getattr(settings, 'ADMIN_SITE_URL', '/')
    
    # Set for default admin site
    admin.site.site_url = url
    
    # Also set for all registered AdminSite instances
    for admin_site in admin.sites.all_sites:
        admin_site.site_url = url
    
    return url 