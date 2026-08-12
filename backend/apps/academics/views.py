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

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.academics.models import Programme
from apps.academics.serializers import ProgrammeStudyPlanSerializer
from apps.academics.services.study_plan import StudyPlanService

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


class ProgrammeStudyPlanView(APIView):
    """
    Return the complete study plan for a programme.
    """

    def get(self, request, programme_id):
        try:
            programme = Programme.objects.get(pk=programme_id)
        except Programme.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": "Programme not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        data = StudyPlanService.generate(programme)

        serializer = ProgrammeStudyPlanSerializer(data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )