from rest_framework import viewsets

from .pagination import StandardResultsSetPagination


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet for all ETU APIs.
    """

    pagination_class = StandardResultsSetPagination

    ordering = ["id"]