from apps.courses.models import CourseRegistration


class CourseRegistrationSelector:

    @staticmethod
    def list_registrations():
        return (
            CourseRegistration.objects
            .select_related(
                "enrollment",
                "course_offering",
                "course_offering__course",
            )
        )

    @staticmethod
    def get_registration(pk):
        return (
            CourseRegistration.objects
            .select_related(
                "enrollment",
                "course_offering",
                "course_offering__course",
            )
            .get(pk=pk)
        )