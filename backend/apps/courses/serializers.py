from rest_framework import serializers

from .models import (
    Course,
    CourseRegistration,
)


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


class CourseRegistrationSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(
        source="enrollment.student_id",
        read_only=True,
    )

    course_code = serializers.CharField(
        source="course_offering.course.code",
        read_only=True,
    )

    course_title = serializers.CharField(
        source="course_offering.course.title",
        read_only=True,
    )

    class Meta:
        model = CourseRegistration
        fields = [
            "id",
            "enrollment",
            "student_id",
            "course_offering",
            "course_code",
            "course_title",
            "status",
            "registered_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "registered_at",
            "created_at",
            "updated_at",
        ]