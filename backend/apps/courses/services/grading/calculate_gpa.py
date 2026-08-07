from decimal import Decimal

from django.db import transaction

from apps.courses.models import (
    AcademicRecord,
    CourseRegistration,
)


class GPAService:

    @staticmethod
    @transaction.atomic
    def calculate(
        enrollment,
        academic_session,
        semester,
    ):
        registrations = CourseRegistration.objects.filter(
            enrollment=enrollment,
            course_offering__academic_session=academic_session,
            course_offering__semester=semester,
            status=CourseRegistration.StatusChoices.APPROVED,
            final_grade__published=True,
        ).select_related(
            "course_offering__course",
            "final_grade",
        )

        total_credit_hours = 0
        earned_credit_hours = 0
        total_grade_points = Decimal("0.00")

        for registration in registrations:
            credits = registration.course_offering.course.credit_hours
            grade = registration.final_grade

            total_credit_hours += credits

            if grade.is_passed:
                earned_credit_hours += credits

            total_grade_points += (
                Decimal(credits) * grade.grade_point
            )

        if total_credit_hours == 0:
            semester_gpa = Decimal("0.00")
        else:
            semester_gpa = (
                total_grade_points /
                Decimal(total_credit_hours)
            ).quantize(Decimal("0.01"))

        standing = AcademicRecord.StandingChoices.GOOD
        remarks = ""

        if semester_gpa < Decimal("1.00"):
            standing = AcademicRecord.StandingChoices.SUSPENSION
            remarks = "Academic Suspension"

        elif semester_gpa < Decimal("2.00"):
            standing = AcademicRecord.StandingChoices.PROBATION
            remarks = "Academic Probation"

        record, created = AcademicRecord.objects.update_or_create(
            enrollment=enrollment,
            academic_session=academic_session,
            semester=semester,
            defaults={
                "total_credit_hours": total_credit_hours,
                "earned_credit_hours": earned_credit_hours,
                "total_grade_points": total_grade_points,
                "semester_gpa": semester_gpa,
                "academic_standing": standing,
                "remarks": remarks,
            },
        )

        records = AcademicRecord.objects.filter(
            enrollment=enrollment,
        )

        total_points = Decimal("0.00")
        total_credits = 0

        for academic_record in records:
            total_points += academic_record.total_grade_points
            total_credits += academic_record.total_credit_hours

        if total_credits > 0:
            cgpa = (
                total_points /
                Decimal(total_credits)
            ).quantize(Decimal("0.01"))
        else:
            cgpa = Decimal("0.00")

        record.cumulative_gpa = cgpa
        record.save(update_fields=["cumulative_gpa"])

        return record