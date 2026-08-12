from django.db import models

from apps.common.models import (
    UUIDModel,
    TimeStampedModel,
)

from apps.courses.models import Course

class Faculty(models.Model):
    code = models.CharField(
        max_length=20,
        unique=True,
    )
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.name


class Department(models.Model):
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="departments",
    )

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.name


class Programme(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="programmes",
    )

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )

    award = models.CharField(
        max_length=50,
    )

    duration_years = models.PositiveIntegerField()

    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.name


class Curriculum(UUIDModel, TimeStampedModel):
    programme = models.ForeignKey(
        Programme,
        on_delete=models.CASCADE,
        related_name="curricula",
    )

    year = models.PositiveIntegerField()
    semester = models.PositiveIntegerField()

    class Meta:
        ordering = ["year", "semester"]
        unique_together = (
            "programme",
            "year",
            "semester",
        )

    def __str__(self):
        return (
            f"{self.programme.name} "
            f"Year {self.year} "
            f"Semester {self.semester}"
        )


class CurriculumCourse(UUIDModel, TimeStampedModel):
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.CASCADE,
        related_name="courses",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    is_core = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            "curriculum",
            "course",
        )

    def __str__(self):
        return (
            f"{self.curriculum} - "
            f"{self.course.code}"
        )