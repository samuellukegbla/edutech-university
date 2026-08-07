from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field

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


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = [
            "id",
            "code",
            "name",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class DepartmentSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(
        source="faculty.name",
        read_only=True,
    )

    class Meta:
        model = Department
        fields = [
            "id",
            "code",
            "name",
            "description",
            "faculty",
            "faculty_name",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class ProgrammeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source="department.name",
        read_only=True,
    )

    faculty_name = serializers.CharField(
        source="department.faculty.name",
        read_only=True,
    )

    class Meta:
        model = Programme
        fields = [
            "id",
            "code",
            "name",
            "award",
            "duration_years",
            "description",
            "department",
            "department_name",
            "faculty_name",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "is_current",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class SemesterSerializer(serializers.ModelSerializer):
    academic_session_name = serializers.CharField(
        source="academic_session.name",
        read_only=True,
    )

    semester_name = serializers.CharField(
        source="get_name_display",
        read_only=True,
    )

    class Meta:
        model = Semester
        fields = [
            "id",
            "academic_session",
            "academic_session_name",
            "name",
            "semester_name",
            "start_date",
            "end_date",
            "is_current",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class StudentApplicationSerializer(serializers.ModelSerializer):
    programme_name = serializers.CharField(
        source="programme.name",
        read_only=True,
    )

    department_name = serializers.CharField(
        source="programme.department.name",
        read_only=True,
    )

    faculty_name = serializers.CharField(
        source="programme.department.faculty.name",
        read_only=True,
    )

    academic_session_name = serializers.CharField(
        source="academic_session.name",
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    gender_display = serializers.CharField(
        source="get_gender_display",
        read_only=True,
    )

    class Meta:
        model = StudentApplication
        fields = [
            "id",
            "application_number",
            "academic_session",
            "academic_session_name",
            "programme",
            "programme_name",
            "department_name",
            "faculty_name",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "gender",
            "gender_display",
            "email",
            "phone_number",
            "nationality",
            "address",
            "status",
            "status_display",
            "submitted_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "application_number",
            "created_at",
            "updated_at",
        )


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    application_number = serializers.CharField(
        source="application.application_number",
        read_only=True,
    )

    document_type_display = serializers.CharField(
        source="get_document_type_display",
        read_only=True,
    )

    class Meta:
        model = ApplicationDocument
        fields = [
            "id",
            "application",
            "application_number",
            "document_type",
            "document_type_display",
            "file",
            "description",
            "verified",
            "verified_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "application_number",
            "verified_at",
            "created_at",
            "updated_at",
        )


class AdmissionDecisionSerializer(serializers.ModelSerializer):
    application_number = serializers.CharField(
        source="application.application_number",
        read_only=True,
    )

    decision_display = serializers.CharField(
        source="get_decision_display",
        read_only=True,
    )

    reviewed_by_username = serializers.CharField(
        source="reviewed_by.username",
        read_only=True,
    )

    class Meta:
        model = AdmissionDecision

        fields = [
            "id",
            "application",
            "application_number",
            "decision",
            "decision_display",
            "review_comments",
            "reviewed_by",
            "reviewed_by_username",
            "decision_date",
            "offer_letter_generated",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "reviewed_by",
            "decision_date",
            "created_at",
            "updated_at",
        )


class EnrollmentSerializer(serializers.ModelSerializer):
    application_number = serializers.CharField(
        source="application.application_number",
        read_only=True,
    )

    student_name = serializers.SerializerMethodField()

    programme_name = serializers.CharField(
        source="programme.name",
        read_only=True,
    )

    academic_session_name = serializers.CharField(
        source="academic_session.name",
        read_only=True,
    )

    semester_name = serializers.CharField(
        source="semester.get_name_display",
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Enrollment

        fields = [
            "id",
            "application",
            "application_number",
            "student_id",
            "student_name",
            "programme",
            "programme_name",
            "academic_session",
            "academic_session_name",
            "semester",
            "semester_name",
            "status",
            "status_display",
            "enrollment_date",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "student_id",
            "enrollment_date",
            "created_at",
            "updated_at",
        )

    @extend_schema_field(str)
    def get_student_name(self, obj):
        return " ".join(
            filter(
                None,
                [
                    obj.application.first_name,
                    obj.application.middle_name,
                    obj.application.last_name,
                ],
            )
        )


class StudentProfileSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(
        source="enrollment.student_id",
        read_only=True,
    )

    student_name = serializers.SerializerMethodField()

    programme_name = serializers.CharField(
        source="enrollment.programme.name",
        read_only=True,
    )

    academic_session_name = serializers.CharField(
        source="enrollment.academic_session.name",
        read_only=True,
    )

    marital_status_display = serializers.CharField(
        source="get_marital_status_display",
        read_only=True,
    )

    class Meta:
        model = StudentProfile

        fields = [
            "id",
            "enrollment",
            "student_id",
            "student_name",
            "programme_name",
            "academic_session_name",
            "profile_photo",
            "national_id_number",
            "passport_number",
            "marital_status",
            "marital_status_display",
            "religion",
            "occupation",
            "emergency_contact_name",
            "emergency_contact_phone",
            "emergency_contact_relationship",
            "guardian_name",
            "guardian_phone",
            "guardian_email",
            "guardian_address",
            "medical_conditions",
            "allergies",
            "blood_group",
            "disability",
            "biography",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    @extend_schema_field(str)
    def get_student_name(self, obj):
        application = obj.enrollment.application

        return " ".join(
            filter(
                None,
                [
                    application.first_name,
                    application.middle_name,
                    application.last_name,
                ],
            )
        )