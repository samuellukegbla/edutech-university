from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.admissions.models import Enrollment
from apps.courses.services import TranscriptService


class TranscriptView(APIView):

    def get(self, request, student_id):

        enrollment = Enrollment.objects.get(
            student_id=student_id
        )

        transcript = TranscriptService.generate(
            enrollment
        )

        return Response(
            transcript,
            status=status.HTTP_200_OK,
        )