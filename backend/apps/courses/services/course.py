from django.db import transaction

from apps.courses.models import Course


class CourseService:
    @staticmethod
    @transaction.atomic
    def create_course(*, validated_data):
        return Course.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update_course(*, course, validated_data):
        for field, value in validated_data.items():
            setattr(course, field, value)

        course.save()
        return course

    @staticmethod
    @transaction.atomic
    def activate_course(*, course):
        course.is_active = True
        course.save(update_fields=["is_active", "updated_at"])
        return course

    @staticmethod
    @transaction.atomic
    def deactivate_course(*, course):
        course.is_active = False
        course.save(update_fields=["is_active", "updated_at"])
        return course