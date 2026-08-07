from apps.courses.models import (
    AcademicRecord,
    CourseRegistration,
)


class TranscriptService:

    @staticmethod
    def generate(enrollment):
        """
        Generate a student's academic transcript.
        """

        records = AcademicRecord.objects.filter(
            enrollment=enrollment,
        ).select_related(
            "academic_session",
            "semester",
        )

        transcript = []

        for record in records:

            registrations = CourseRegistration.objects.filter(
                enrollment=enrollment,
                course_offering__academic_session=record.academic_session,
                course_offering__semester=record.semester,
                final_grade__published=True,
            ).select_related(
                "course_offering__course",
                "final_grade",
            )

            courses = []

            for registration in registrations:

                courses.append({
                    "course_code": registration.course_offering.course.code,
                    "course_title": registration.course_offering.course.title,
                    "credit_hours": registration.course_offering.course.credit_hours,
                    "letter_grade": registration.final_grade.letter_grade,
                    "grade_point": registration.final_grade.grade_point,
                })

            transcript.append({
                "academic_session": str(record.academic_session),
                "semester": str(record.semester),
                "semester_gpa": record.semester_gpa,
                "cumulative_gpa": record.cumulative_gpa,
                "standing": record.academic_standing,
                "courses": courses,
            })

        return transcript