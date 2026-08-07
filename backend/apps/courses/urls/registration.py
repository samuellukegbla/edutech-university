from rest_framework.routers import DefaultRouter

from apps.courses.views.registration import CourseRegistrationViewSet

router = DefaultRouter()

router.register(
    r"course-registrations",
    CourseRegistrationViewSet,
    basename="course-registration",
)

urlpatterns = router.urls