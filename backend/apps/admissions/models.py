from django.db import models

from apps.common.models import UUIDModel, TimeStampedModel


class Faculty(UUIDModel, TimeStampedModel):
    code = models.CharField(max_length=10, unique=True)
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

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("faculty", "name")
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

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)

    duration_years = models.PositiveSmallIntegerField(default=4)

    award = models.CharField(
        max_length=100,
        help_text="Example: BSc, BA, Diploma, MSc",
    )

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Programme"
        verbose_name_plural = "Programmes"

class Programme(UUIDModel, TimeStampedModel):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="programmes",
    )

    code = models.CharField(max_length=20, unique=True)
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

    def __str__(self):
        return f"{self.code} - {self.name}"