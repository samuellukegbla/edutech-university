from django.db.models import Sum
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.courses.models import (
    Assessment,
    StudentAssessment,
    FinalGrade,
    GradeScale,
)


class FinalGradeService:

    @staticmethod
    @transaction.atomic
    def calculate(course_registration):

        expected = Assessment.objects.filter(
            course_offering=course_registration.course_offering,
            is_published=True,
        ).count()

        recorded = StudentAssessment.objects.filter(
            course_registration=course_registration,
        ).count()

        if expected != recorded:
            raise ValidationError(
                "Not all assessments have been graded for this course."
            )

        # Calculate total score
        total_score = (
            StudentAssessment.objects.filter(
                course_registration=course_registration,
            ).aggregate(
                total=Sum("score")
            )["total"]
            or 0
        )

        # Find matching grade scale
        grade_scale = (
            GradeScale.objects.filter(
                is_active=True,
                minimum_score__lte=total_score,
                maximum_score__gte=total_score,
            )
            .order_by("-minimum_score")
            .first()
        )

        if grade_scale is None:
            raise ValidationError(
                f"No active grade scale found for score {total_score}."
            )

        # Create or update final grade
        final_grade, _ = FinalGrade.objects.update_or_create(
            course_registration=course_registration,
            defaults={
                "final_score": total_score,
                "letter_grade": grade_scale.letter_grade,
                "grade_point": grade_scale.grade_point,
                "is_passed": grade_scale.is_pass,
                "remarks": grade_scale.remarks,
            },
        )

        return final_grade