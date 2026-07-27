from django.core.exceptions import ValidationError
from django.db import models

from apps.common.models import UUIDModel, TimeStampedModel
from apps.admissions.models import Department, Programme

from django.conf import settings
from apps.admissions.models import AcademicSession, Semester

from apps.admissions.models import Enrollment

from django.utils import timezone


class Course(UUIDModel, TimeStampedModel):
    class SemesterChoices(models.TextChoices):
        FIRST = "FIRST", "First Semester"
        SECOND = "SECOND", "Second Semester"
        SUMMER = "SUMMER", "Summer"

    class LevelChoices(models.IntegerChoices):
        LEVEL_100 = 100, "100 Level"
        LEVEL_200 = 200, "200 Level"
        LEVEL_300 = 300, "300 Level"
        LEVEL_400 = 400, "400 Level"
        LEVEL_500 = 500, "500 Level"

    class CourseTypeChoices(models.TextChoices):
        CORE = "CORE", "Core"
        ELECTIVE = "ELECTIVE", "Elective"

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="courses",
    )

    programme = models.ForeignKey(
        Programme,
        on_delete=models.PROTECT,
        related_name="courses",
    )

    credit_hours = models.PositiveSmallIntegerField()

    level = models.PositiveSmallIntegerField(
    choices=LevelChoices.choices,
    )

    semester = models.CharField(
        max_length=10,
        choices=SemesterChoices.choices,
    )

    course_type = models.CharField(
        max_length=20,
        choices=CourseTypeChoices.choices,
        default=CourseTypeChoices.CORE,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["level", "code"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.code} - {self.title}"
    

class CoursePrerequisite(UUIDModel, TimeStampedModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="prerequisites",
    )

    prerequisite = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="required_for",
    )

    def clean(self):
        if self.course == self.prerequisite:
            raise ValidationError(
                "A course cannot be a prerequisite of itself."
        )

    class Meta:
        unique_together = (
            "course",
            "prerequisite",
        )

        verbose_name = "Course Prerequisite"
        verbose_name_plural = "Course Prerequisites"

    def __str__(self):
        return f"{self.course.code} requires {self.prerequisite.code}"


class ProgrammeCurriculum(UUIDModel, TimeStampedModel):
    programme = models.ForeignKey(
        Programme,
        on_delete=models.CASCADE,
        related_name="curriculum",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="curricula",
    )

    level = models.PositiveSmallIntegerField(
        choices=Course.LevelChoices.choices,
    )

    semester = models.CharField(
        max_length=10,
        choices=Course.SemesterChoices.choices,
    )

    is_required = models.BooleanField(
        default=True,
        help_text="Required or elective course",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["programme", "course"],
                name="unique_programme_course",
            )
        ]

        ordering = [
            "programme",
            "level",
            "semester",
            "course__code",
        ]

        verbose_name = "Programme Curriculum"
        verbose_name_plural = "Programme Curricula"

    def __str__(self):
        return f"{self.programme.name} - {self.course.code}"


class CourseOffering(UUIDModel, TimeStampedModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="offerings",
    )

    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.PROTECT,
        related_name="course_offerings",
    )

    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name="course_offerings",
    )

    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="course_offerings",
    )

    maximum_students = models.PositiveIntegerField(
        default=100,
    )

    registration_open = models.DateField()

    registration_close = models.DateField()

    is_active = models.BooleanField(
        default=True,
    )

    def clean(self):
        if self.registration_open > self.registration_close:
           raise ValidationError(
               "Registration open date cannot be after the close date."
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "course",
                    "academic_session",
                    "semester",
                ],
                name="unique_course_offering",
            )
        ]

        ordering = [
            "course__code",
        ]

        verbose_name = "Course Offering"
        verbose_name_plural = "Course Offerings"

    def __str__(self):
        return (
            f"{self.course.code} - "
            f"{self.academic_session.name} "
            f"({self.semester.name})"
        )


class CourseRegistration(UUIDModel, TimeStampedModel):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        DROPPED = "DROPPED", "Dropped"
        REJECTED = "REJECTED", "Rejected"

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="course_registrations",
    )

    course_offering = models.ForeignKey(
        CourseOffering,
        on_delete=models.PROTECT,
        related_name="registrations",
    )

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )

    registered_at = models.DateTimeField(
        auto_now_add=True,
    )

    def clean(self):
        today = timezone.now().date()

        if not (
            self.course_offering.registration_open
            <= today
            <= self.course_offering.registration_close
        ):
            raise ValidationError(
                "Registration for this course is currently closed."
        )

        if not self.enrollment.is_active:
            raise ValidationError(
                "Inactive students cannot register for courses."
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["enrollment", "course_offering"],
                name="unique_course_registration",
            )
        ]

        ordering = ["-registered_at"]

        verbose_name = "Course Registration"
        verbose_name_plural = "Course Registrations"

    def __str__(self):
        return (
            f"{self.enrollment.student_id} - "
            f"{self.course_offering.course.code}"
        )


class AssessmentType(UUIDModel, TimeStampedModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    default_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Percentage contribution (e.g. 20.00)",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Assessment Type"
        verbose_name_plural = "Assessment Types"

    def __str__(self):
        return self.name
    

class Assessment(UUIDModel, TimeStampedModel):
    course_offering = models.ForeignKey(
        CourseOffering,
        on_delete=models.CASCADE,
        related_name="assessments",
    )

    assessment_type = models.ForeignKey(
        AssessmentType,
        on_delete=models.PROTECT,
        related_name="assessments",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    total_marks = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=100.00,
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Percentage contribution to final grade",
    )

    due_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_published = models.BooleanField(
        default=False,
    )

    def clean(self):
        if self.weight <= 0 or self.weight > 100:
            raise ValidationError(
                "Assessment weight must be between 0 and 100."
        )

    class Meta:
        ordering = [
            "course_offering",
            "due_date",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "course_offering",
                    "title",
                ],
                name="unique_assessment_title_per_course_offering",
            )
        ]

        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"

    def __str__(self):
        return (
            f"{self.course_offering.course.code} - "
            f"{self.title}"
        )
    
class StudentAssessment(UUIDModel, TimeStampedModel):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="student_assessments",
    )

    course_registration = models.ForeignKey(
        CourseRegistration,
        on_delete=models.CASCADE,
        related_name="assessments",
    )

    score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    is_absent = models.BooleanField(
        default=False,
    )

    feedback = models.TextField(
        blank=True,
    )

    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="graded_assessments",
    )

    graded_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "assessment",
                    "course_registration",
                ],
                name="unique_student_assessment",
            )
        ]

        ordering = [
            "assessment",
            "course_registration",
        ]

        verbose_name = "Student Assessment"
        verbose_name_plural = "Student Assessments"
    
    def clean(self):
        if self.score < 0:
            raise ValidationError(
                "Score cannot be negative."
        )

        if self.score > self.assessment.total_marks:
            raise ValidationError(
                "Score cannot exceed the total marks."
        )

    
    def save(self, *args, **kwargs):
        if self.graded_by and self.graded_at is None:
            self.graded_at = timezone.now()

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.course_registration.enrollment.student_id} - "
            f"{self.assessment.title}"
        )
    

class FinalGrade(UUIDModel, TimeStampedModel):
    class LetterGrade(models.TextChoices):
        A = "A", "A"
        B_PLUS = "B+", "B+"
        B = "B", "B"
        C_PLUS = "C+", "C+"
        C = "C", "C"
        D = "D", "D"
        F = "F", "F"

    course_registration = models.OneToOneField(
        CourseRegistration,
        on_delete=models.CASCADE,
        related_name="final_grade",
    )

    final_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    letter_grade = models.CharField(
        max_length=2,
        choices=LetterGrade.choices,
    )

    grade_point = models.DecimalField(
        max_digits=3,
        decimal_places=2,
    )

    is_passed = models.BooleanField(
        default=True,
    )

    remarks = models.CharField(
        max_length=255,
        blank=True,
    )

    published = models.BooleanField(
        default=False,
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = [
            "course_registration",
        ]

        verbose_name = "Final Grade"
        verbose_name_plural = "Final Grades"

    def save(self, *args, **kwargs):
        if self.published and self.published_at is None:
           self.published_at = timezone.now()

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.course_registration.enrollment.student_id}"
            f" - {self.letter_grade}"
        )
    

class GradeScale(UUIDModel, TimeStampedModel):
    letter_grade = models.CharField(
        max_length=5,
        unique=True,
    )

    minimum_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    maximum_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    grade_point = models.DecimalField(
        max_digits=3,
        decimal_places=2,
    )

    remarks = models.CharField(
        max_length=100,
        blank=True,
    )

    is_pass = models.BooleanField(
        default=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["-minimum_score"]
        verbose_name = "Grade Scale"
        verbose_name_plural = "Grade Scales"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.minimum_score > self.maximum_score:
            raise ValidationError(
                "Minimum score cannot be greater than maximum score."
            )

    def __str__(self):
        return (
            f"{self.letter_grade} "
            f"({self.minimum_score}-{self.maximum_score})"
        )


class AcademicRecord(UUIDModel, TimeStampedModel):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="academic_records",
    )

    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.PROTECT,
        related_name="academic_records",
    )

    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name="academic_records",
    )

    total_credit_hours = models.PositiveIntegerField(
        default=0,
    )

    earned_credit_hours = models.PositiveIntegerField(
        default=0,
    )

    total_grade_points = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    semester_gpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
    )

    cumulative_gpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
    )

    class StandingChoices(models.TextChoices):
        GOOD = "GOOD", "Good Standing"
        PROBATION = "PROBATION", "Academic Probation"
        SUSPENSION = "SUSPENSION", "Academic Suspension"

    academic_standing = models.CharField(
        max_length=20,
        choices=StandingChoices.choices,
        default=StandingChoices.GOOD,
    )

    remarks = models.CharField(
        max_length=255,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "enrollment",
                    "academic_session",
                    "semester",
                ],
                name="unique_academic_record",
            )
        ]

        ordering = [
            "enrollment",
            "-academic_session",
            "-semester",
        ]

        verbose_name = "Academic Record"
        verbose_name_plural = "Academic Records"

    def __str__(self):
        return (
            f"{self.enrollment.student_id} - "
            f"{self.academic_session} - "
            f"{self.semester}"
        )