from apps.admissions.models import Enrollment
from apps.academics.services.transcript import TranscriptService
from apps.academics.services.degree_progress import DegreeProgressService
from apps.courses.models import CourseRegistration


class StudentDashboardService:

    @staticmethod
    def generate(enrollment):

        transcript = TranscriptService.generate(
            enrollment
        )

        audit = DegreeProgressService.generate(
            enrollment
        )

        registered_courses = (
            CourseRegistration.objects.filter(
                enrollment=enrollment
            ).count()
        )

        completed_courses = len(
            [
                c
                for c in audit["courses"]
                if c["completed"]
            ]
        )

        pending_courses = (
            len(audit["courses"])
            - completed_courses
        )

        return {
            "student_id": enrollment.student_id,
            "programme": enrollment.programme.name,
            "academic_session":
                enrollment.academic_session.name,
            "semester":
                enrollment.semester.get_name_display(),
            "cgpa": transcript["cgpa"],
            "registered_courses":
                registered_courses,
            "completed_courses":
                completed_courses,
            "pending_courses":
                pending_courses,
            "completion_percentage":
                audit["completion_percentage"],
        }