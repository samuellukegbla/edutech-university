import django_filters

from .models import Course

from .models import CourseRegistration


class CourseFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(
        field_name="code",
        lookup_expr="icontains",
    )

    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
    )

    department = django_filters.UUIDFilter(
        field_name="department",
    )

    programme = django_filters.UUIDFilter(
        field_name="programme",
    )

    level = django_filters.NumberFilter(
        field_name="level",
    )

    semester = django_filters.CharFilter(
        field_name="semester",
    )

    course_type = django_filters.CharFilter(
        field_name="course_type",
    )

    is_active = django_filters.BooleanFilter(
        field_name="is_active",
    )

    class Meta:
        model = Course
        fields = [
            "code",
            "title",
            "department",
            "programme",
            "level",
            "semester",
            "course_type",
            "is_active",
        ]


class CourseRegistrationFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(
        field_name="status",
        lookup_expr="iexact",
    )

    enrollment = django_filters.UUIDFilter(
        field_name="enrollment",
    )

    course_offering = django_filters.UUIDFilter(
        field_name="course_offering",
    )

    class Meta:
        model = CourseRegistration
        fields = [
            "status",
            "enrollment",
            "course_offering",
        ]