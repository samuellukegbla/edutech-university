from django.contrib import admin

from .models import (
    Course,
    CoursePrerequisite,
    ProgrammeCurriculum,
    CourseOffering,
    CourseRegistration,
    AssessmentType,
    Assessment,
    StudentAssessment,
    FinalGrade,
    GradeScale,
    AcademicRecord,
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "title",
        "programme",
        "department",
        "level",
        "semester",
        "credit_hours",
        "course_type",
        "is_active",
    )

    list_filter = (
        "programme",
        "department",
        "level",
        "semester",
        "course_type",
        "is_active",
    )

    search_fields = (
        "code",
        "title",
    )

    ordering = (
        "level",
        "code",
    )


@admin.register(CoursePrerequisite)
class CoursePrerequisiteAdmin(admin.ModelAdmin):
    list_display = (
        "course",
        "prerequisite",
    )

    search_fields = (
        "course__code",
        "prerequisite__code",
    )

    autocomplete_fields = (
        "course",
        "prerequisite",
    )


@admin.register(ProgrammeCurriculum)
class ProgrammeCurriculumAdmin(admin.ModelAdmin):
    list_display = (
        "programme",
        "course",
        "level",
        "semester",
        "is_required",
    )

    list_filter = (
        "programme",
        "level",
        "semester",
        "is_required",
    )

    search_fields = (
        "programme__name",
        "course__code",
        "course__title",
    )

    autocomplete_fields = (
        "programme",
        "course",
    )

    ordering = (
        "programme",
        "level",
        "semester",
    )


@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = (
        "course",
        "academic_session",
        "semester",
        "lecturer",
        "maximum_students",
        "is_active",
    )

    list_filter = (
        "academic_session",
        "semester",
        "is_active",
    )

    search_fields = (
        "course__code",
        "course__title",
    )

    autocomplete_fields = (
        "course",
        "academic_session",
        "semester",
        "lecturer",
    )

    ordering = (
        "course",
    )


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "enrollment",
        "course_offering",
        "status",
        "registered_at",
    )

    list_filter = (
        "status",
        "registered_at",
    )

    search_fields = (
        "enrollment__student_id",
        "course_offering__course__code",
        "course_offering__course__title",
    )

    readonly_fields = (
        "registered_at",
    )

    autocomplete_fields = (
        "enrollment",
        "course_offering",
    )

    ordering = (
        "-registered_at",
    )


@admin.register(AssessmentType)
class AssessmentTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "default_weight",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course_offering",
        "assessment_type",
        "weight",
        "total_marks",
        "due_date",
        "is_published",
    )

    list_filter = (
        "assessment_type",
        "is_published",
    )

    search_fields = (
        "title",
        "course_offering__course__code",
        "course_offering__course__title",
    )

    autocomplete_fields = (
        "course_offering",
        "assessment_type",
    )

    ordering = (
        "course_offering",
        "due_date",
    )


@admin.register(StudentAssessment)
class StudentAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "course_registration",
        "assessment",
        "score",
        "is_absent",
        "graded_by",
        "graded_at",
    )

    list_filter = (
        "assessment",
        "is_absent",
    )

    search_fields = (
        "course_registration__enrollment__student_id",
        "assessment__title",
    )

    autocomplete_fields = (
        "assessment",
        "course_registration",
        "graded_by",
    )

@admin.register(FinalGrade)
class FinalGradeAdmin(admin.ModelAdmin):
    list_display = (
        "course_registration",
        "final_score",
        "letter_grade",
        "grade_point",
        "is_passed",
        "published",
    )

    list_filter = (
        "letter_grade",
        "is_passed",
        "published",
    )

    search_fields = (
        "course_registration__enrollment__student_id",
    )

    autocomplete_fields = (
        "course_registration",
    )


@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = (
        "letter_grade",
        "minimum_score",
        "maximum_score",
        "grade_point",
        "is_pass",
        "is_active",
    )

    list_filter = (
        "is_pass",
        "is_active",
    )

    search_fields = (
        "letter_grade",
    )

    ordering = (
        "-minimum_score",
    )


@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = (
        "enrollment",
        "academic_session",
        "semester",
        "semester_gpa",
        "cumulative_gpa",
        "academic_standing",
    )

    list_filter = (
        "academic_session",
        "semester",
        "academic_standing",
    )

    search_fields = (
        "enrollment__student_id",
    )

    autocomplete_fields = (
        "enrollment",
        "academic_session",
        "semester",
    )