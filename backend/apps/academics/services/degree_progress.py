from decimal import Decimal

from apps.courses.models import CourseRegistration

from apps.academics.models import Programme as AcademicProgramme

class DegreeProgressService:

    @staticmethod
    def generate(enrollment):
        """
        Generate a degree progress audit for a student enrollment.
        """

        programme = AcademicProgramme.objects.get(
            code=enrollment.programme.code
        )

        curricula = (
            programme.curricula
            .prefetch_related(
                "courses__course"
            )
            .all()
        )

        required_credit_hours = Decimal("0")
        completed_credit_hours = Decimal("0")

        completed_course_ids = set()

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

        for registration in registrations:
            final_grade = registration.final_grade

            if final_grade.is_passed:
                course = registration.course_offering.course

                completed_course_ids.add(course.id)

                completed_credit_hours += Decimal(
                    str(course.credit_hours)
                )

        courses = []

        for curriculum in curricula:
            for curriculum_course in curriculum.courses.all():

                course = curriculum_course.course

                required_credit_hours += Decimal(
                    str(course.credit_hours)
                )

                completed = course.id in completed_course_ids

                courses.append(
                    {
                        "year": curriculum.year,
                        "semester": curriculum.semester,
                        "course_id": str(course.id),
                        "course_code": course.code,
                        "course_title": course.title,
                        "credit_hours": course.credit_hours,
                        "is_core": curriculum_course.is_core,
                        "completed": completed,
                    }
                )

        remaining_credit_hours = (
            required_credit_hours - completed_credit_hours
        )

        if required_credit_hours > 0:
            completion_percentage = (
                completed_credit_hours
                / required_credit_hours
                * Decimal("100")
            )
        else:
            completion_percentage = Decimal("0")

        return {
            "student_id": enrollment.student_id,
            "programme": {
                "id": str(programme.id),
                "code": programme.code,
                "name": programme.name,
                "award": programme.award,
            },
            "required_credit_hours": required_credit_hours,
            "completed_credit_hours": completed_credit_hours,
            "remaining_credit_hours": remaining_credit_hours,
            "completion_percentage": completion_percentage,
            "courses": courses,
        }