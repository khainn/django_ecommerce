import os
from pathlib import Path

from decouple import config
import django.conf.locale
from django.utils.translation import gettext_lazy as _

DEBUG = False
BASE_DIR = Path(__file__).parent.parent.parent.absolute()

SECRET_KEY = config('DJANGO_SECRET_KEY', cast=str)
JWT_TOKEN_EXPIRE_HOURS = config('JWT_TOKEN_EXPIRE_HOURS', cast=int, default=1)
JWT_REFRESH_TOKEN_EXPIRE_DAYS = config('JWT_REFRESH_TOKEN_EXPIRE_DAYS', cast=int, default=1)
ALLOWED_HOSTS = ["django-ecommerce-lhsn.onrender.com"]
CSRF_TRUSTED_ORIGINS = ["https://django-ecommerce-lhsn.onrender.com"]

# Cloudinary configuration
CLOUDINARY = {
    'cloud_name': config('CLOUDINARY_CLOUD_NAME', cast=str),
    'api_key': config('CLOUDINARY_API_KEY', cast=str),
    'api_secret': config('CLOUDINARY_API_SECRET', cast=str),
    'secure': True
}

# Use this setting for allowing all origins in CORS
APPEND_SLASH = True
CORS_ALLOW_ALL_ORIGINS = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
CORS_EXPOSE_HEADERS = ['Content-Disposition']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'cloudinary_storage',
    'apps.ecommerce'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.ecommerce.context_processors.admin_site_url',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME', cast=str),
        'USER': config('DATABASE_USER', cast=str),
        'PASSWORD': config('DATABASE_PASSWORD', cast=str),
        'HOST': config('DATABASE_HOST', cast=str),
        'PORT': config('DATABASE_PORT', cast=int)
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ['email'],
            'max_similarity': 0.7,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Extra places for collectstatic to find static files - simpler approach
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files (Uploaded images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

# Cloudinary storage configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', cast=str),
    'API_KEY': config('CLOUDINARY_API_KEY', cast=str),
    'API_SECRET': config('CLOUDINARY_API_SECRET', cast=str),
    'STATIC_IMAGES_EXTENSIONS': ['jpg', 'jpe', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'tif', 'tiff', 'ico'],
    'MAGIC_FILE_PATH': 'magic',
    'STATIC_IMAGES_TRANSFORMATIONS': {
        'default': {
            'quality': 'auto',
            'fetch_format': 'auto',
        }
    }
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

LANGUAGE_CODE = 'vi'
LANGUAGES = [
    ('en', 'English'),
    ('vi', 'Tiếng Việt'),
]

TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Comment out the AUTH_USER_MODEL line to use the default Django User model
# AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user_login': '60/min',
    },
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'common.exceptions.api_error_handler',
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.CustomPagination',
    'PAGE_SIZE': 10
}

DATA_UPLOAD_MAX_MEMORY_SIZE = config('DATA_UPLOAD_MAX_MEMORY_SIZE', cast=int, default=25 * 1024 * 1024)
FILE_UPLOAD_MAX_MEMORY_SIZE = config('FILE_UPLOAD_MAX_MEMORY_SIZE', cast=int, default=25 * 1024 * 1024)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# API documentation settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'E-commerce API Documentation',
    'DESCRIPTION': 'API documentation for the E-commerce application',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    # Enable UI in production
    # 'SWAGGER_UI_SETTINGS': {
    #     'deepLinking': True,
    #     'persistAuthorization': True,
    #     'displayOperationId': True,
    # },
    # Allow all to access the API docs (you can customize this for more restricted access)
    # 'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
}


# Handle multiple external hosts
EXTERNAL_HOST = config('EXTERNAL_HOST', cast=str, default='')
if EXTERNAL_HOST:
    ALLOWED_HOSTS.extend([host.strip() for host in EXTERNAL_HOST.split(',')])

ADMIN_SITE_URL = config('ADMIN_SITE_URL', cast=str, default='')
ADMIN_VIEW_SITE_TEXT = config('ADMIN_VIEW_SITE_TEXT', cast=str, default='STORE')

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Jazzmin Settings
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Store manager",
    # Title on the login screen (19 chars max) (Will default to current_admin_site.site_header if absent or None)
    "site_header": "Store manager",
    # Title on the brand (19 chars max) (Will default to current_admin_site.site_header if absent or None)
    "site_brand": "Store manager",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": None,
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    # Welcome text on the login screen
    "welcome_sign": "Welcome to Store Manager",
    # Copyright on the footer
    "copyright": "Store Manager",
    # Hide the search bar on the topbar
    "show_search": False,
    # The model admin to search from the search bar, search bar omitted if excluded
    # "search_model": "ecommerce.Product",
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": ADMIN_SITE_URL or "/", "new_window": True},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # List of apps
    "order_with_respect_to": [
        'ecommerce.Banner',
        'ecommerce.Product',
        'ecommerce.ProductCategory',
        'ecommerce.Blog',
        'ecommerce.BlogImage',
        'ecommerce.Order',
        'ecommerce.Cart',
        'ecommerce.CartItem',
    ],
    # Custom icons for side menu apps/models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    # Hide these apps from the sidebar menu
    "hide_apps": ["auth", "authtoken"],
    # Hide these models from the sidebar menu
    "hide_models": ["auth.Group", "auth.User"],
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS files (must be present in static files)
    "custom_css": "css/admin_vietnamese_font.css",
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    # Hide the version number
    "show_version": False,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "language_chooser": True
}

# UI Customizer
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

for lang in django.conf.locale.LANG_INFO.values():
    if lang.get('code') == 'vi':
        lang['name_local'] = 'Tiếng Việt'

# Add this to ensure language cookie is set properly
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = None  # Cookie expires when browser closes
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_PATH = '/'
LANGUAGE_COOKIE_SECURE = True
LANGUAGE_COOKIE_HTTPONLY = True
LANGUAGE_COOKIE_SAMESITE = 'Lax'
