from decimal import Decimal

from apps.courses.models import (
    FinalGrade,
    CourseRegistration,
)
from rest_framework import serializers

class TranscriptService:
    @staticmethod
    def generate(enrollment):
        registrations = (
            CourseRegistration.objects
            .filter(
                enrollment=enrollment,
                status="APPROVED",
                final_grade__published=True,
            )
            .select_related(
                "course_offering__course",
                "final_grade",
            )
        )

        transcript = []
        total_credits = Decimal("0")
        total_grade_points = Decimal("0")

        for registration in registrations:
            course = registration.course_offering.course
            grade = registration.final_grade

            credits = course.credit_hours
            points = grade.grade_point

            total_credits += credits
            total_grade_points += (
                points * credits
            )

            transcript.append(
                {
                    "course_code": course.code,
                    "course_title": course.title,
                    "credit_hours": credits,
                    "letter_grade": grade.letter_grade,
                    "grade_points": points,
                }
            )

        cgpa = (
            total_grade_points / total_credits
            if total_credits > 0
            else Decimal("0")
        )

        return {
            "student_id": enrollment.student_id,
            "programme": enrollment.programme.name,
            "total_credits": total_credits,
            "cgpa": round(cgpa, 2),
            "courses": transcript,
        }


class TranscriptSerializer(serializers.Serializer):
    student_id = serializers.CharField()
    programme = serializers.CharField()
    total_credits = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    cgpa = serializers.DecimalField(
        max_digits=4,
        decimal_places=2
    )
    courses = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )