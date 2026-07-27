from decimal import Decimal

from apps.courses.models import FinalGrade


class GPACalculator:
    @staticmethod
    def calculate(enrollment, academic_session, semester):
        grades = FinalGrade.objects.filter(
            course_registration__enrollment=enrollment,
            course_registration__course_offering__academic_session=academic_session,
            course_registration__course_offering__semester=semester,
            published=True,
        ).select_related(
            "course_registration__course_offering__course"
        )

        total_grade_points = Decimal("0")
        total_credit_hours = 0

        for grade in grades:
            course = grade.course_registration.course_offering.course

            total_grade_points += (
                grade.grade_point * course.credit_hours
            )

            total_credit_hours += course.credit_hours

        if total_credit_hours == 0:
            return Decimal("0.00")

        return round(
            total_grade_points / Decimal(total_credit_hours),
            2,
        )