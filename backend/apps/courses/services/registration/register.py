from apps.courses.models import CourseRegistration


class CourseRegistrationService:

    @staticmethod
    def create_registration(validated_data):
        return CourseRegistration.objects.create(**validated_data)

    @staticmethod
    def update_registration(
        registration,
        validated_data,
    ):
        for key, value in validated_data.items():
            setattr(registration, key, value)

        registration.save()

        return registration