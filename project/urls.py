from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from apps.ecommerce.admin import ecommerce_admin
from project.health import health_check

urlpatterns = [
    path('admin/', ecommerce_admin.urls),
    path('django-admin/', admin.site.urls),
    path('api/ecommerce/', include('apps.ecommerce.api.urls')),
    path('api/health/', health_check, name='health_check'),
]
if settings.DEBUG:
    urlpatterns += [
        path('api/schema', SpectacularAPIView.as_view(), name='schema'),
        path('api/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        path('api/swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
