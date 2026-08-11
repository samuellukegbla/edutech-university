from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FacultyViewSet,
    DepartmentViewSet,
    ProgrammeViewSet,
)

router = DefaultRouter()

router.register(
    "faculties",
    FacultyViewSet,
)

router.register(
    "departments",
    DepartmentViewSet,
)

router.register(
    "programmes",
    ProgrammeViewSet,
)

urlpatterns = [
    path("", include(router.urls)),
]