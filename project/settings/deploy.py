import os
from pathlib import Path

from decouple import config

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
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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
STATICFILES_DIRS = []

# Media files (Uploaded images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

# Cloudinary storage configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', cast=str),
    'API_KEY': config('CLOUDINARY_API_KEY', cast=str),
    'API_SECRET': config('CLOUDINARY_API_SECRET', cast=str),
    'STATIC_IMAGES_EXTENSIONS': ['jpg', 'jpe', 'jpeg', 'png'],
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
LANGUAGES = [
    ('en', 'English'),
    ('ja', 'Japanese'),
]
LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
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
