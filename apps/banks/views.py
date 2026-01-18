from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.banks.models import Bank
from apps.banks.serializers import BankSerializer


class BankViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Bank model.
    Provides: list, create, retrieve, update, partial_update, destroy
    """
    queryset = Bank.objects.filter(deleted_at__isnull=True)
    serializer_class = BankSerializer
    
    # Filtering
    filterset_fields = ['type_bank']
    
    # Search
    search_fields = ['name', 'address']
    
    # Ordering
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']

    def perform_destroy(self, instance):
        """Soft delete instead of hard delete."""
        instance.soft_delete()
