from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from apps.common.viewsets import BaseModelViewSet

from .services import EnrollmentService

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

from .serializers import (
    FacultySerializer,
    DepartmentSerializer,
    ProgrammeSerializer,
    AcademicSessionSerializer,
    SemesterSerializer,
    StudentApplicationSerializer,
    ApplicationDocumentSerializer,
    AdmissionDecisionSerializer,
    EnrollmentSerializer,
    StudentProfileSerializer,
)


class FacultyViewSet(BaseModelViewSet):
    queryset = Faculty.objects.all()

    serializer_class = FacultySerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "is_active",
    ]

    search_fields = [
        "code",
        "name",
    ]

    ordering_fields = [
        "code",
        "name",
        "created_at",
    ]

    ordering = [
        "name",
    ]


class DepartmentViewSet(BaseModelViewSet):
    queryset = (
        Department.objects
        .select_related("faculty")
        .all()
    )

    serializer_class = DepartmentSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "faculty",
        "is_active",
    ]

    search_fields = [
        "code",
        "name",
    ]

    ordering_fields = [
        "code",
        "name",
        "created_at",
    ]

    ordering = [
        "name",
    ]


class ProgrammeViewSet(BaseModelViewSet):
    queryset = (
        Programme.objects
        .select_related("department__faculty")
        .all()
    )

    serializer_class = ProgrammeSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "department",
        "award",
        "is_active",
    ]

    search_fields = [
        "code",
        "name",
    ]

    ordering_fields = [
        "code",
        "name",
        "duration_years",
        "created_at",
    ]

    ordering = [
        "name",
    ]


class AcademicSessionViewSet(BaseModelViewSet):
    queryset = AcademicSession.objects.all()

    serializer_class = AcademicSessionSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "is_current",
        "is_active",
    ]

    search_fields = [
        "name",
    ]

    ordering_fields = [
        "name",
        "start_date",
        "end_date",
        "created_at",
    ]

    ordering = [
        "-start_date",
    ]


class SemesterViewSet(BaseModelViewSet):
    queryset = (
        Semester.objects
        .select_related("academic_session")
        .all()
    )

    serializer_class = SemesterSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "academic_session",
        "name",
        "is_current",
        "is_active",
    ]

    search_fields = [
        "academic_session__name",
    ]

    ordering_fields = [
        "start_date",
        "end_date",
        "created_at",
    ]

    ordering = [
        "start_date",
    ]


class StudentApplicationViewSet(BaseModelViewSet):
    queryset = (
        StudentApplication.objects
        .select_related(
            "programme",
            "programme__department",
            "programme__department__faculty",
            "academic_session",
        )
        .all()
    )

    serializer_class = StudentApplicationSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "programme",
        "academic_session",
    ]

    search_fields = [
        "application_number",
        "first_name",
        "last_name",
        "email",
    ]

    ordering_fields = [
        "application_number",
        "submitted_at",
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]


class ApplicationDocumentViewSet(BaseModelViewSet):
    queryset = (
        ApplicationDocument.objects
        .select_related("application")
        .all()
    )

    serializer_class = ApplicationDocumentSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "document_type",
        "verified",
    ]

    search_fields = [
        "application__application_number",
    ]

    ordering_fields = [
        "document_type",
        "verified_at",
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]


class AdmissionDecisionViewSet(BaseModelViewSet):
    queryset = (
        AdmissionDecision.objects
        .select_related(
            "application",
            "reviewed_by",
        )
        .all()
    )

    serializer_class = AdmissionDecisionSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "decision",
        "offer_letter_generated",
    ]

    search_fields = [
        "application__application_number",
        "application__first_name",
        "application__last_name",
    ]

    ordering_fields = [
        "decision_date",
        "created_at",
    ]

    ordering = [
        "-decision_date",
    ]


class EnrollmentViewSet(BaseModelViewSet):
    queryset = (
        Enrollment.objects.select_related(
            "application",
            "programme",
            "academic_session",
            "semester",
        )
        .all()
    )

    serializer_class = EnrollmentSerializer

    search_fields = [
        "student_id",
        "application__application_number",
        "application__first_name",
        "application__middle_name",
        "application__last_name",
    ]

    filterset_fields = [
        "programme",
        "academic_session",
        "semester",
        "status",
    ]

    ordering_fields = [
        "student_id",
        "enrollment_date",
        "created_at",
    ]

    ordering = ["student_id"]

    def perform_create(self, serializer):
        EnrollmentService.create_enrollment(serializer)


class StudentProfileViewSet(BaseModelViewSet):
    queryset = (
        StudentProfile.objects.select_related(
            "enrollment",
            "enrollment__application",
            "enrollment__programme",
            "enrollment__academic_session",
        )
        .all()
    )

    serializer_class = StudentProfileSerializer

    search_fields = [
        "enrollment__student_id",
        "enrollment__application__first_name",
        "enrollment__application__middle_name",
        "enrollment__application__last_name",
        "national_id_number",
        "passport_number",
    ]

    filterset_fields = [
        "marital_status",
        "blood_group",
    ]

    ordering_fields = [
        "enrollment__student_id",
        "created_at",
    ]

    ordering = [
        "enrollment__student_id",
    ]

    def perform_create(self, serializer):
        StudentProfileService.create_student_profile(serializer)