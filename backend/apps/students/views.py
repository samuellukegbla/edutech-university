from rest_framework.views import APIView
from rest_framework.response import Response

from apps.admissions.models import Enrollment
from apps.students.services.dashboard import (
    StudentDashboardService,
)
from apps.students.services.portal import StudentPortalService


class StudentDashboardAPIView(APIView):

    def get(self, request, student_id):

        enrollment = Enrollment.objects.get(
            student_id=student_id
        )

        data = StudentDashboardService.generate(
            enrollment
        )

        return Response(data)


class StudentPortalAPIView(APIView):

    def get(self, request, student_id):

        enrollment = Enrollment.objects.get(
            student_id=student_id
        )

        data = StudentPortalService.generate(
            enrollment
        )

        return Response(data)