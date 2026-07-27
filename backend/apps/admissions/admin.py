from django.contrib import admin

from .models import (
    Faculty, 
    Department, 
    Programme, 
    AcademicSession, 
    Semester, 
    StudentApplication, 
    ApplicationDocument, 
    AdmissionDecision,  
    Enrollment,
    StudentProfile,
)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "faculty",
        "is_active",
    )

    list_filter = (
        "faculty",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "department",
        "award",
        "duration_years",
        "is_active",
    )

    list_filter = (
        "department",
        "award",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    ordering = (
        "name",
    )


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
        "end_date",
        "is_current",
        "is_active",
    )

    list_filter = (
        "is_current",
        "is_active",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "-start_date",
    )


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = (
        "academic_session",
        "name",
        "start_date",
        "end_date",
        "is_current",
        "is_active",
    )

    list_filter = (
        "academic_session",
        "name",
        "is_current",
        "is_active",
    )

    search_fields = (
        "academic_session__name",
    )

    ordering = (
        "academic_session",
        "start_date",
    )


@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "application_number",
        "first_name",
        "last_name",
        "programme",
        "academic_session",
        "status",
    )

    list_filter = (
        "status",
        "academic_session",
        "programme",
    )

    search_fields = (
        "application_number",
        "first_name",
        "last_name",
        "email",
    )

    readonly_fields = (
        "application_number",
    )


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "document_type",
        "verified",
        "verified_at",
    )

    list_filter = (
        "document_type",
        "verified",
    )

    search_fields = (
        "application__application_number",
    )

    autocomplete_fields = (
        "application",
    )


@admin.register(AdmissionDecision)
class AdmissionDecisionAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "decision",
        "reviewed_by",
        "decision_date",
        "offer_letter_generated",
    )

    list_filter = (
        "decision",
        "offer_letter_generated",
    )

    search_fields = (
        "application__application_number",
        "application__first_name",
        "application__last_name",
    )

    autocomplete_fields = (
        "application",
        "reviewed_by",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "application",
        "programme",
        "academic_session",
        "semester",
        "enrollment_date",
        "status",
    )

    list_filter = (
        "academic_session",
        "semester",
        "status",
    )

    search_fields = (
        "student_id",
        "application__application_number",
        "application__first_name",
        "application__last_name",
    )

    autocomplete_fields = (
        "application",
        "programme",
        "academic_session",
        "semester",
    )

    readonly_fields = (
        "student_id",
        "enrollment_date",
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "enrollment",
        "guardian_name",
        "emergency_contact_name",
    )

    search_fields = (
        "enrollment__student_id",
        "guardian_name",
    )

    autocomplete_fields = (
        "enrollment",
    )