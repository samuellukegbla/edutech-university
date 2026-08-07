from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from apps.common.pagination import StandardResultsSetPagination

from apps.courses.filters import CourseFilter
from apps.courses.models import Course
from apps.courses.selectors import CourseSelector
from apps.courses.serializers import CourseSerializer
from apps.courses.services import CourseService


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

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

    def get_queryset(self):
        return CourseSelector.list_courses()

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