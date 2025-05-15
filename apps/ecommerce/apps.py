from django.apps import AppConfig
import os


class EcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ecommerce'
    
    def ready(self):
        # Create templates directory structure if it doesn't exist
        templates_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'templates')
        admin_dir = os.path.join(templates_dir, 'admin')
        
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
        if not os.path.exists(admin_dir):
            os.makedirs(admin_dir) 