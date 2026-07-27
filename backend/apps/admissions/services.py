from django.db import transaction

from .models import Enrollment


class EnrollmentService:
    @staticmethod
    @transaction.atomic
    def create_enrollment(serializer):
        """
        Create a new enrollment.
        Additional business logic can be added here in the future.
        """
        enrollment = serializer.save()
        return enrollment


class StudentProfileService:
    @staticmethod
    @transaction.atomic
    def create_student_profile(serializer):
        """
        Create a student profile.

        Additional business logic can be added here later.
        """
        profile = serializer.save()
        return profile