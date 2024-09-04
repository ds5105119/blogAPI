# https://docs.djangoproject.com/en/5.1/topics/http/urls/
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[AllowAny]
)

urlpatterns = [
    path("", include("api.urls")),
]

if settings.ADMIN_ENABLED is True:
    urlpatterns += [
        path("admin/", admin.site.urls),
        path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    ]
