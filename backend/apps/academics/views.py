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


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ProgrammeViewSet(viewsets.ModelViewSet):
    queryset = Programme.objects.all()
    serializer_class = ProgrammeSerializer