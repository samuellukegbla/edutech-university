from apps.courses.models import AcademicRecord


class AcademicStandingService:

    @staticmethod
    def determine(gpa):
        if gpa >= 2.0:
            return AcademicRecord.StandingChoices.GOOD

        if gpa >= 1.0:
            return AcademicRecord.StandingChoices.PROBATION

        return AcademicRecord.StandingChoices.SUSPENSION