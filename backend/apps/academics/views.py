from rest_framework import viewsets

from .models import (
    Faculty,
    Department,
    Programme,
)

from .serializers import (
    FacultySerializer,
    DepartmentSerializer,
    ProgrammeSerializer,
)

from apps.academics.models import (
    Curriculum,
    CurriculumCourse,
)

from apps.academics.serializers import (
    CurriculumSerializer,
    CurriculumCourseSerializer,
)


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ProgrammeViewSet(viewsets.ModelViewSet):
    queryset = Programme.objects.all()
    serializer_class = ProgrammeSerializer


class CurriculumViewSet(
    viewsets.ModelViewSet
):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer


class CurriculumCourseViewSet(
    viewsets.ModelViewSet
):
    queryset = CurriculumCourse.objects.all()
    serializer_class = CurriculumCourseSerializer