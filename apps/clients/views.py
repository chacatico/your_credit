from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.clients.models import Client
from apps.clients.serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Client model.
    Provides: list, create, retrieve, update, partial_update, destroy
    """
    queryset = Client.objects.filter(deleted_at__isnull=True).select_related('bank')
    serializer_class = ClientSerializer
    
    # Filtering
    filterset_fields = ['person_type', 'bank', 'nationality']
    
    # Search by client name
    search_fields = ['full_name', 'email', 'phone']
    
    # Ordering
    ordering_fields = ['full_name', 'created_at', 'age']
    ordering = ['-created_at']

    def perform_destroy(self, instance):
        """Soft delete instead of hard delete."""
        instance.soft_delete()