from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.common.models import UUIDModel, TimeStampedModel

from django.core.validators import RegexValidator


class Faculty(UUIDModel, TimeStampedModel):
    code = models.CharField(
    max_length=10,
    unique=True,
    db_index=True,
)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"

    def __str__(self):
        return f"{self.code} - {self.name}"


class Department(UUIDModel, TimeStampedModel):
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="departments",
    )

    code = models.CharField(
    max_length=20,
    unique=True,
    db_index=True,
)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["faculty", "name"],
                name="unique_department_name_per_faculty",
            )
       ]

        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return f"{self.faculty.code} - {self.name}"


class Programme(UUIDModel, TimeStampedModel):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="programmes",
    )

    code = models.CharField(
    max_length=20,
    unique=True,
    db_index=True,
)
    name = models.CharField(max_length=200)

    award = models.CharField(
        max_length=50,
        help_text="Example: Certificate, Diploma, BSc, BA, BEng, MSc, MBA"
    )

    duration_years = models.PositiveSmallIntegerField(default=4)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Programme"
        verbose_name_plural = "Programmes"

    def __str__(self):
        return f"{self.code} - {self.name}"

class AcademicSession(UUIDModel, TimeStampedModel):
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text="Example: 2026/2027"
    )

    start_date = models.DateField()
    end_date = models.DateField()

    is_current = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Academic Session"
        verbose_name_plural = "Academic Sessions"

    def clean(self):
        super().clean()

        if self.end_date <= self.start_date:
            raise ValidationError({
                "end_date": "End date must be after the start date."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Semester(UUIDModel, TimeStampedModel):
    class SemesterChoices(models.TextChoices):
        FIRST = "FIRST", "First Semester"
        SECOND = "SECOND", "Second Semester"
        SUMMER = "SUMMER", "Summer Semester"

    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name="semesters",
    )

    name = models.CharField(
        max_length=20,
        choices=SemesterChoices.choices,
    )

    start_date = models.DateField()
    end_date = models.DateField()

    is_current = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["academic_session", "start_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["academic_session", "name"],
                name="unique_semester_per_session",
            )
        ]
        verbose_name = "Semester"
        verbose_name_plural = "Semesters"

    def __str__(self):
        return f"{self.academic_session.name} - {self.get_name_display()}"

    def clean(self):
        super().clean()

        if self.end_date <= self.start_date:
            raise ValidationError({
                "end_date": "End date must be after the start date."
            })

        if (
            self.start_date < self.academic_session.start_date
            or self.end_date > self.academic_session.end_date
        ):
            raise ValidationError({
                "start_date": (
                    "Semester dates must fall within the academic session."
                )
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    

class StudentApplication(UUIDModel, TimeStampedModel):
    class GenderChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    class StatusChoices(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"
        WAITLISTED = "WAITLISTED", "Waitlisted"
        DEFERRED = "DEFERRED", "Deferred"

    application_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
        db_index=True,
    )

    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.PROTECT,
        related_name="applications",
    )

    programme = models.ForeignKey(
        Programme,
        on_delete=models.PROTECT,
        related_name="applications",
    )

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
    )

    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    nationality = models.CharField(max_length=100)
    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Student Application"
        verbose_name_plural = "Student Applications"
    
    def save(self, *args, **kwargs):
        if not self.application_number:
            year = timezone.now().year

            last = StudentApplication.objects.filter(
                application_number__startswith=f"ETU-{year}"
            ).count() + 1

            self.application_number = f"ETU-{year}-{last:06d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.application_number} - "
            f"{self.first_name} {self.middle_name} {self.last_name}"
    )


class ApplicationDocument(UUIDModel, TimeStampedModel):
    class DocumentType(models.TextChoices):
        PASSPORT = "PASSPORT", "Passport Photograph"
        NATIONAL_ID = "NATIONAL_ID", "National ID"
        BIRTH_CERTIFICATE = "BIRTH_CERTIFICATE", "Birth Certificate"
        WASSCE = "WASSCE", "WASSCE/WAEC Result"
        TRANSCRIPT = "TRANSCRIPT", "Academic Transcript"
        RECOMMENDATION = "RECOMMENDATION", "Recommendation Letter"
        OTHER = "OTHER", "Other"

    application = models.ForeignKey(
        StudentApplication,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
    )

    file = models.FileField(
        upload_to="applications/documents/",
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    verified = models.BooleanField(default=False)

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["document_type"]
        verbose_name = "Application Document"
        verbose_name_plural = "Application Documents"

    def __str__(self):
        return f"{self.application.application_number} - {self.get_document_type_display()}"


class AdmissionDecision(UUIDModel, TimeStampedModel):
    class DecisionChoices(models.TextChoices):
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"
        WAITLISTED = "WAITLISTED", "Waitlisted"
        DEFERRED = "DEFERRED", "Deferred"

    application = models.OneToOneField(
        StudentApplication,
        on_delete=models.CASCADE,
        related_name="decision",
    )

    decision = models.CharField(
        max_length=20,
        choices=DecisionChoices.choices,
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admission_reviews",
    )

    review_comments = models.TextField(blank=True)

    decision_date = models.DateTimeField(auto_now_add=True)

    offer_letter_generated = models.BooleanField(default=False)

    class Meta:
        ordering = ["-decision_date"]
        verbose_name = "Admission Decision"
        verbose_name_plural = "Admission Decisions"

    def __str__(self):
        return f"{self.application.application_number} - {self.get_decision_display()}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.application.status = self.decision
        self.application.save(update_fields=["status"])


class Enrollment(UUIDModel, TimeStampedModel):
    application = models.OneToOneField(
        StudentApplication,
        on_delete=models.PROTECT,
        related_name="enrollment",
    )

    student_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        db_index=True,
    )

    programme = models.ForeignKey(
        Programme,
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    enrollment_date = models.DateField(
        auto_now_add=True,
    )

    class EnrollmentStatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        DEFERRED = "DEFERRED", "Deferred"
        SUSPENDED = "SUSPENDED", "Suspended"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"
        GRADUATED = "GRADUATED", "Graduated"

    status = models.CharField(
        max_length=20,
        choices=EnrollmentStatusChoices.choices,
        default=EnrollmentStatusChoices.ACTIVE,
    )

    def clean(self):
        super().clean()

        if not self.application_id:
            return

        if self.application.status != StudentApplication.StatusChoices.ACCEPTED:
            raise ValidationError(
                {
                    "application": (
                        "Only accepted applications can be enrolled."
                    )
                }
            )

        if self.programme != self.application.programme:
            raise ValidationError(
                {
                    "programme": (
                        "Programme must match the student's application."
                    )
                }
            )

        if self.academic_session != self.application.academic_session:
            raise ValidationError(
                {
                    "academic_session": (
                        "Academic session must match the student's application."
                    )
                }
            )

        if self.semester.academic_session != self.academic_session:
            raise ValidationError(
                {
                    "semester": (
                        "Selected semester does not belong to the selected academic session."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.student_id:
            year = timezone.now().year

            last = Enrollment.objects.filter(
                student_id__startswith=f"ETU{year}"
            ).count() + 1

            self.student_id = f"ETU{year}{last:05d}"

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["student_id"]
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"

        indexes = [
            models.Index(fields=["programme"]),
            models.Index(fields=["academic_session"]),
            models.Index(fields=["semester"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        full_name = " ".join(
            filter(
                None,
                [
                    self.application.first_name,
                    self.application.middle_name,
                    self.application.last_name,
                ],
            )
        )
        return f"{self.student_id} - {full_name}"


class StudentProfile(UUIDModel, TimeStampedModel):
    class MaritalStatusChoices(models.TextChoices):
        SINGLE = "SINGLE", "Single"
        MARRIED = "MARRIED", "Married"
        DIVORCED = "DIVORCED", "Divorced"
        WIDOWED = "WIDOWED", "Widowed"

    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    profile_photo = models.ImageField(
        upload_to="students/profile_photos/",
        blank=True,
        null=True,
    )

    national_id_number = models.CharField(
        max_length=50,
        blank=True,
        db_index=True,
    )

    passport_number = models.CharField(
        max_length=50,
        blank=True,
        db_index=True,
    )

    marital_status = models.CharField(
        max_length=20,
        choices=MaritalStatusChoices.choices,
        default=MaritalStatusChoices.SINGLE,
    )

    religion = models.CharField(
        max_length=100,
        blank=True,
    )

    occupation = models.CharField(
        max_length=150,
        blank=True,
    )

    phone_validator = RegexValidator(
        regex=r"^\+?[0-9]{7,15}$",
        message="Enter a valid phone number.",
    )

    emergency_contact_name = models.CharField(
        max_length=150,
    )

    emergency_contact_phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
    )

    emergency_contact_relationship = models.CharField(
        max_length=100,
    )

    guardian_name = models.CharField(
        max_length=150,
    )

    guardian_phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
    )

    guardian_email = models.EmailField(
        blank=True,
    )

    guardian_address = models.TextField(
        blank=True,
    )

    medical_conditions = models.TextField(
        blank=True,
    )

    allergies = models.TextField(
        blank=True,
    )

    class BloodGroupChoices(models.TextChoices):
        A_POS = "A+", "A+"
        A_NEG = "A-", "A-"
        B_POS = "B+", "B+"
        B_NEG = "B-", "B-"
        AB_POS = "AB+", "AB+"
        AB_NEG = "AB-", "AB-"
        O_POS = "O+", "O+"
        O_NEG = "O-", "O-"

    blood_group = models.CharField(
        max_length=3,
        choices=BloodGroupChoices.choices,
        blank=True,
    )

    disability = models.TextField(
        blank=True,
    )

    biography = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["enrollment__student_id"]
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"

        indexes = [
            models.Index(fields=["marital_status"]),
            models.Index(fields=["passport_number"]),
        ]

    def __str__(self):
        application = self.enrollment.application

        full_name = " ".join(
            filter(
                None,
                [
                    application.first_name,
                    application.middle_name,
                    application.last_name,
                ],
            )
        )

        return f"{self.enrollment.student_id} - {full_name}"


