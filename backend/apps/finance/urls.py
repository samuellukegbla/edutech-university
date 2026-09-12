from rest_framework.routers import DefaultRouter

from .views import (
    FeeStructureViewSet,
    InvoiceViewSet,
    PaymentViewSet,
    ScholarshipViewSet,
)

router = DefaultRouter()

router.register(
    "fees",
    FeeStructureViewSet
)

router.register(
    "invoices",
    InvoiceViewSet
)

router.register(
    "payments",
    PaymentViewSet
)

router.register(
    "scholarships",
    ScholarshipViewSet
)

urlpatterns = router.urls