from django.db import models


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