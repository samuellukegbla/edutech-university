from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.academics.views import (
    FacultyViewSet,
    DepartmentViewSet,
    ProgrammeViewSet,
    CurriculumViewSet,
    CurriculumCourseViewSet,
    ProgrammeStudyPlanView,
    TranscriptAPIView,
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
    "curriculum-courses",
    CurriculumCourseViewSet,
    basename="curriculum-course",
)

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += [
    path(
        "programmes/<int:programme_id>/study-plan/",
        ProgrammeStudyPlanView.as_view(),
        name="programme-study-plan",
    ),
    path(
        "transcript/<str:student_id>/",
        TranscriptAPIView.as_view(),
        name="transcript",
    ),
]