from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FacultyViewSet,
    DepartmentViewSet,
    ProgrammeViewSet,
    CurriculumViewSet,
    CurriculumCourseViewSet,
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

router.register(
    r"curricula",
    CurriculumViewSet,
)

router.register(
    r"curriculum-courses",
    CurriculumCourseViewSet,
)

urlpatterns = [
    path("", include(router.urls)),
]