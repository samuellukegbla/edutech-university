from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from apps.common.pagination import StandardResultsSetPagination

from .filters import CourseFilter
from .models import Course
from .selectors import CourseSelector
from .serializers import CourseSerializer
from .services import CourseService


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    queryset = CourseSelector.list_courses()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = CourseFilter

    search_fields = [
        "code",
        "title",
        "description",
    ]

    ordering_fields = [
        "code",
        "title",
        "credit_hours",
        "level",
    ]

    ordering = [
        "level",
        "code",
    ]

    def perform_create(self, serializer):
        course = CourseService.create_course(
            validated_data=serializer.validated_data,
        )
        serializer.instance = course

    def perform_update(self, serializer):
        course = CourseService.update_course(
            course=self.get_object(),
            validated_data=serializer.validated_data,
        )
        serializer.instance = course