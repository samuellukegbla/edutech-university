from django.db import models
from apps.admissions.models import Enrollment


class FeeStructure(models.Model):
    programme = models.CharField(max_length=200)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.programme


class Invoice(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="invoices"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    paid = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Invoice #{self.id}"


class Payment(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    reference = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.reference


class Scholarship(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=255
    )

    percentage = models.PositiveIntegerField()

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name