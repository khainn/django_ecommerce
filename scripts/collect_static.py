#!/usr/bin/env python
import os
import django
import sys
from decouple import config

# Add the project directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django with the correct settings module based on PRODUCTION flag
is_production = config('PRODUCTION', cast=bool, default=False)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
                      'project.settings.deploy' if is_production else 'project.settings.dev')

django.setup()

from django.core.management import call_command
from django.conf import settings

def collect_static():
    """Collect static files"""
    print("Collecting static files...")
    try:
        # Create the STATIC_ROOT directory if it doesn't exist
        os.makedirs(settings.STATIC_ROOT, exist_ok=True)
        
        call_command('collectstatic', '--noinput', verbosity=1)
        print(f"Static files collected successfully to {settings.STATIC_ROOT}!")
        
        # Print a warning if we're in production mode but WhiteNoise isn't installed
        if is_production:
            try:
                import whitenoise
                print(f"WhiteNoise  is installed for serving static files in production.")
            except ImportError:
                print("WARNING: WhiteNoise is not installed. Static files may not be served correctly in production.")
                print("Install WhiteNoise with: pip install whitenoise")
    except Exception as e:
        print(f"An error occurred while collecting static files: {e}")

if __name__ == '__main__':
    collect_static() 