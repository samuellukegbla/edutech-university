from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


DEFAULT_FILTER_BACKENDS = [
    DjangoFilterBackend,
    filters.SearchFilter,
    filters.OrderingFilter,
]