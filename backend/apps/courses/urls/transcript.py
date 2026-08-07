from django.urls import path

from apps.courses.views.transcript import TranscriptView

urlpatterns = [
    path(
        "transcript/<str:student_id>/",
        TranscriptView.as_view(),
        name="student-transcript",
    ),
]