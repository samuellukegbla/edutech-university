from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # Students API
    path(
        "api/v1/students/",
        include("apps.students.urls"),
    ),

    # Courses API
    path(
        "api/v1/",
        include("apps.courses.urls"),
    ),

    # Admissions API
    path(
        "api/v1/admissions/",
        include("apps.admissions.urls"),
    ),

    # API Documentation
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "api/v1/academics/",
        include("apps.academics.urls"),
    ),
    path(
        "api/finance/",
        include("apps.finance.urls")
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )