from apps.academics.services.degree_progress import (
    DegreeProgressService,
)
from apps.academics.services.transcript import (
    TranscriptService,
)
from apps.courses.models import CourseRegistration


class StudentPortalService:

    @staticmethod
    def generate(enrollment):

        progress = DegreeProgressService.generate(
            enrollment
        )

        transcript = TranscriptService.generate(
            enrollment
        )

        registrations = (
            CourseRegistration.objects
            .filter(
                enrollment=enrollment,
                status="APPROVED",
            )
            .select_related(
                "course_offering__course"
            )
        )

        current_courses = []

        for registration in registrations:
            current_courses.append({
                "code": registration.course_offering.course.code,
                "title": registration.course_offering.course.title,
            })

        application = enrollment.application

        return {
            "student": {
                "student_id": enrollment.student_id,
                "name": (
                    f"{application.first_name} "
                    f"{application.last_name}"
                ),
                "programme": enrollment.programme.name,
            },

            "dashboard": {
                "completion_percentage":
                    progress["completion_percentage"],
                "completed_courses":
                    len([
                        c for c in progress["courses"]
                        if c["completed"]
                    ]),
            },

            "transcript": {
                "cgpa": transcript["cgpa"],
                "total_credits":
                    transcript["total_credits"],
            },

            "current_courses":
                current_courses,
        }