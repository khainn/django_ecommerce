#!/usr/bin/env python
import os
import sys

import django
from decouple import config
from django.conf import settings
from django.core.management import call_command

# Add the project directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django with the correct settings module based on PRODUCTION flag
is_production = config("PRODUCTION", cast=bool, default=False)
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "project.settings.deploy" if is_production else "project.settings.dev")

django.setup()

def collect_static():
    """Collect static files"""
    os.makedirs(settings.STATIC_ROOT, exist_ok=True)

    call_command("collectstatic", "--noinput", verbosity=1)

    if is_production:
        pass


if __name__ == "__main__":
    collect_static()
