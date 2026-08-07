from apps.courses.models import CourseRegistration
from .validation import RegistrationValidationService


class CourseRegistrationService:

    @staticmethod
    def register_student(
        enrollment,
        course_offering,
    ):
        RegistrationValidationService.validate(
            enrollment=enrollment,
            course_offering=course_offering,
        )

        return CourseRegistration.objects.create(
            enrollment=enrollment,
            course_offering=course_offering,
        )

    @staticmethod
    def update_registration(
        registration,
        validated_data,
    ):
        for key, value in validated_data.items():
            setattr(registration, key, value)

        registration.save()

        return registration