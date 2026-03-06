from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ===============================
# Root API View
# ===============================

@api_view(['GET'])
def api_root(request):
    return Response({
        "message": "Reader's Hub API is running"
    })


# ===============================
# Swagger Configuration
# ===============================

schema_view = get_schema_view(
    openapi.Info(
        title="Reader's Hub API",
        default_version='v1',
        description="API for book lovers to track reading, write reviews, and connect with others",
        contact=openapi.Contact(email="contact@readershug.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# ===============================
# URL Patterns
# ===============================

urlpatterns = [
    path('', api_root),

    path('admin/', admin.site.urls),

    path('api/accounts/', include('accounts.urls')),
    path('api/books/', include('books.urls')),
    path('api/activities/', include('activities.urls')),
    path('api/comments/', include('comments.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0)),
]

# ===============================
# Media Files (Development Only)
# ===============================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )