from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone

from apps.courses.models import (
    CourseRegistration,
    FinalGrade,
)

class RegistrationValidationService:
    """
    Business rules for student course registration.
    """

    MAX_CREDIT_HOURS = 18

    @classmethod
    def validate(
        cls,
        enrollment,
        course_offering,
    ):
        cls.validate_student_status(enrollment)
        cls.validate_registration_window(course_offering)
        cls.validate_duplicate_registration(
            enrollment,
            course_offering,
        )
        cls.validate_programme(
            enrollment,
            course_offering,
        )
        cls.validate_credit_limit(
            enrollment,
            course_offering,
        )
        cls.validate_prerequisites(
            enrollment,
            course_offering,
        )

    @staticmethod
    def validate_student_status(enrollment):
        if (
            enrollment.status
            != enrollment.StatusChoices.ACTIVE
        ):
            raise ValidationError(
                "Only active students can register for courses."
            )

    @staticmethod
    def validate_registration_window(course_offering):
        today = timezone.now().date()

        if not (
            course_offering.registration_open
            <= today
            <= course_offering.registration_close
        ):
            raise ValidationError(
                "Course registration is closed."
            )

    @staticmethod
    def validate_duplicate_registration(
        enrollment,
        course_offering,
    ):
        if CourseRegistration.objects.filter(
            enrollment=enrollment,
            course_offering=course_offering,
        ).exists():
            raise ValidationError(
                "You have already registered for this course."
            )

    @staticmethod
    def validate_programme(
        enrollment,
        course_offering,
    ):
        if (
            enrollment.programme
            != course_offering.course.programme
        ):
            raise ValidationError(
                "This course does not belong to your programme."
            )

    @classmethod
    def validate_credit_limit(
        cls,
        enrollment,
        course_offering,
    ):
        current = (
            CourseRegistration.objects.filter(
                enrollment=enrollment,
            )
            .select_related("course_offering__course")
            .aggregate(
                total=Sum(
                    "course_offering__course__credit_hours"
                )
            )["total"]
            or 0
        )

        total = (
            current
            + course_offering.course.credit_hours
        )

        if total > cls.MAX_CREDIT_HOURS:
            raise ValidationError(
                f"Maximum credit load is {cls.MAX_CREDIT_HOURS}."
            )

    @staticmethod
    def validate_prerequisites(
        enrollment,
        course_offering,
    ):
        """
        Ensure all prerequisite courses have been passed.
        """

        prerequisites = (
            course_offering.course.prerequisites.select_related(
                "prerequisite"
            )
        )

        for item in prerequisites:
            passed = FinalGrade.objects.filter(
                course_registration__enrollment=enrollment,
                course_registration__course_offering__course=item.prerequisite,
                is_passed=True,
            ).exists()

            if not passed:
                raise ValidationError(
                    f"You must pass "
                    f"{item.prerequisite.code} "
                    f"before registering for "
                    f"{course_offering.course.code}."
                )