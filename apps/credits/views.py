from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.credits.models import Credit
from apps.credits.serializers import CreditSerializer


class CreditViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Credit model.
    Provides: list, create, retrieve, update, partial_update, destroy
    """
    queryset = Credit.objects.filter(deleted_at__isnull=True).select_related('client', 'bank')
    serializer_class = CreditSerializer
    
    # Filtering by credit type and bank
    filterset_fields = ['credit_type', 'bank', 'client']
    
    # Search by description and client name
    search_fields = ['description', 'client__full_name']
    
    # Ordering
    ordering_fields = ['registration_date', 'minimum_payment', 'maximum_payment', 'term_months']
    ordering = ['-registration_date']

    def perform_destroy(self, instance):
        """Soft delete instead of hard delete."""
        instance.soft_delete()
