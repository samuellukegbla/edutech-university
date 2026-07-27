from rest_framework.routers import DefaultRouter

from .views import (
    FacultyViewSet,
    DepartmentViewSet,
    ProgrammeViewSet,
    AcademicSessionViewSet,
    SemesterViewSet,
    StudentApplicationViewSet,
    ApplicationDocumentViewSet,
    AdmissionDecisionViewSet,
    EnrollmentViewSet,
    StudentProfileViewSet,
)

router = DefaultRouter()

router.register(
    r"faculties",
    FacultyViewSet,
    basename="faculty",
)

router.register(
    r"departments",
    DepartmentViewSet,
    basename="department",
)

router.register(
    r"programmes",
    ProgrammeViewSet,
    basename="programme",
)

router.register(
    r"academic-sessions",
    AcademicSessionViewSet,
    basename="academic-session",
)

router.register(
    r"semesters",
    SemesterViewSet,
    basename="semester",
)

router.register(
    r"applications",
    StudentApplicationViewSet,
    basename="student-application",
)

router.register(
    r"application-documents",
    ApplicationDocumentViewSet,
    basename="application-document",
)

router.register(
    r"admission-decisions",
    AdmissionDecisionViewSet,
    basename="admission-decision",
)

router.register(
    r"enrollments",
    EnrollmentViewSet,
    basename="enrollment",
)

router.register(
    r"student-profiles",
    StudentProfileViewSet,
    basename="student-profile",
)

urlpatterns = router.urls