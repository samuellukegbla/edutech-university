from django.db.models import QuerySet

from apps.courses.models import Course


class CourseSelector:
    @staticmethod
    def list_courses() -> QuerySet:
        return (
            Course.objects.select_related(
                "department",
                "programme",
            ).order_by("level", "code")
        )

    @staticmethod
    def get_course_by_id(course_id):
        return (
            Course.objects.select_related(
                "department",
                "programme",
            ).get(pk=course_id)
        )

    @staticmethod
    def active_courses() -> QuerySet:
        return (
            Course.objects.filter(
                is_active=True,
            )
            .select_related(
                "department",
                "programme",
            )
            .order_by("level", "code")
        )