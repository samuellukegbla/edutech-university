from django.contrib import admin

from .models import Faculty, Department, Programme, AcademicSession


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