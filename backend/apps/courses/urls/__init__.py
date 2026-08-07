from django.urls import include, path

urlpatterns = [
    path("", include("apps.courses.urls.course")),
    path("", include("apps.courses.urls.registration")),
    path("", include("apps.courses.urls.transcript")),
]