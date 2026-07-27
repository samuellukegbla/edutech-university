from rest_framework import serializers

from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source="department.name",
        read_only=True,
    )

    programme_name = serializers.CharField(
        source="programme.name",
        read_only=True,
    )

    class Meta:
        model = Course
        fields = (
            "id",
            "code",
            "title",
            "description",
            "department",
            "department_name",
            "programme",
            "programme_name",
            "credit_hours",
            "level",
            "semester",
            "course_type",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )