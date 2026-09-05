from django.urls import path

from apps.students.views import (
    StudentDashboardAPIView, 
    StudentPortalAPIView,
)

urlpatterns = [
    path(
        "dashboard/<str:student_id>/",
        StudentDashboardAPIView.as_view(),
        name="student-dashboard",
    ),
    path(
        "portal/<str:student_id>/",
        StudentPortalAPIView.as_view(),
        name="student-portal",
    ),
]
