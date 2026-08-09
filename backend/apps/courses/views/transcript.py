from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from apps.admissions.models import Enrollment
from apps.courses.serializers.transcript import TranscriptSerializer
from apps.courses.services import TranscriptService

from django.shortcuts import get_object_or_404


class TranscriptView(APIView):

    @extend_schema(
        summary="Generate Student Transcript",
        description=(
            "Returns the student's academic transcript, "
            "including semester GPA, cumulative GPA, "
            "academic standing, and published courses."
        ),
        responses=TranscriptSerializer(many=True),
    )
    def get(self, request, student_id):

        enrollment = get_object_or_404(
            Enrollment,
            student_id=student_id,
        )

        transcript = TranscriptService.generate(
            enrollment
        )

        serializer = TranscriptSerializer(
            transcript,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )