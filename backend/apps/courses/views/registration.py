from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from apps.common.pagination import StandardResultsSetPagination

from apps.courses.filters import CourseRegistrationFilter
from apps.courses.selectors import CourseRegistrationSelector
from apps.courses.serializers import CourseRegistrationSerializer
from apps.courses.services import CourseRegistrationService


class CourseRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = CourseRegistrationSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = CourseRegistrationFilter

    search_fields = [
        "enrollment__student_id",
        "course_offering__course__code",
        "course_offering__course__title",
    ]

    ordering_fields = [
        "registered_at",
        "status",
    ]

    ordering = [
        "-registered_at",
    ]

    def get_queryset(self):
        return CourseRegistrationSelector.list_registrations()

    def perform_create(self, serializer):
        registration = CourseRegistrationService.register_student(
            enrollment=serializer.validated_data["enrollment"],
            course_offering=serializer.validated_data["course_offering"],
        )

        serializer.instance = registration

    def perform_update(self, serializer):
        registration = CourseRegistrationService.update_registration(
            registration=self.get_object(),
            validated_data=serializer.validated_data,
        )

        serializer.instance = registration