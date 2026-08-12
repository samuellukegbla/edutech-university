from collections import defaultdict

from apps.academics.models import CurriculumCourse


class StudyPlanService:

    @staticmethod
    def generate(programme):
        """
        Generate the complete study plan for a programme.

        Structure:
        Programme
            Year
                Semester
                    Courses
        """

        curriculum_courses = (
            CurriculumCourse.objects
            .filter(curriculum__programme=programme)
            .select_related(
                "curriculum",
                "course",
            )
            .order_by(
                "curriculum__year",
                "curriculum__semester",
                "course__code",
            )
        )

        years = defaultdict(lambda: defaultdict(list))

        total_programme_credit_hours = 0

        for item in curriculum_courses:
            credit_hours = item.course.credit_hours

            total_programme_credit_hours += credit_hours

            years[item.curriculum.year][item.curriculum.semester].append(
                {
                    "id": str(item.course.id),
                    "code": item.course.code,
                    "title": item.course.title,
                    "credit_hours": credit_hours,
                    "is_core": item.is_core,
                }
            )

        study_plan = []

        for year, semesters in sorted(years.items()):

            year_data = {
                "year": year,
                "semesters": [],
            }

            for semester, courses in sorted(semesters.items()):

                semester_credit_hours = sum(
                    course["credit_hours"]
                    for course in courses
                )

                year_data["semesters"].append(
                    {
                        "semester": semester,
                        "total_credit_hours": semester_credit_hours,
                        "courses": courses,
                    }
                )

            study_plan.append(year_data)

        return {
            "programme": {
                "id": programme.id,
                "code": programme.code,
                "name": programme.name,
                "award": programme.award,
                "duration_years": programme.duration_years,
                "total_credit_hours": total_programme_credit_hours,
            },
            "study_plan": study_plan,
        }