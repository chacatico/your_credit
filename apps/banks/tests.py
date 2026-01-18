import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.banks.models import Bank


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username='testuser',
        password='testpass123'
    )
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def bank():
    return Bank.objects.create(
        name='Test Bank',
        type_bank='PRIVATE',
        address='123 Test Street'
    )


@pytest.mark.django_db
class TestBankModel:
    """Tests for Bank model."""

    def test_bank_creation(self):
        """Test creating a bank instance."""
        bank = Bank.objects.create(
            name='Sample Bank',
            type_bank='PRIVATE',
            address='456 Main Ave'
        )
        assert bank.name == 'Sample Bank'
        assert bank.type_bank == 'PRIVATE'
        assert str(bank) == 'Sample Bank'

    def test_bank_soft_delete(self, bank):
        """Test soft delete functionality."""
        bank.soft_delete()
        assert bank.is_deleted is True
        assert bank.deleted_at is not None

    def test_bank_restore(self, bank):
        """Test restoring a soft-deleted bank."""
        bank.soft_delete()
        bank.restore()
        assert bank.is_deleted is False
        assert bank.deleted_at is None


@pytest.mark.django_db
class TestBankSerializer:
    """Tests for Bank serializer validations."""

    def test_valid_bank_data(self, authenticated_client):
        """Test creating bank with valid data."""
        url = reverse('bank-list')
        data = {
            'name': 'New Bank',
            'type_bank': 'GOVERNMENT',
            'address': '789 Gov Street'
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_empty_name_validation(self, authenticated_client):
        """Test that empty name is rejected."""
        url = reverse('bank-list')
        data = {
            'name': '   ',
            'type_bank': 'PRIVATE',
            'address': '123 Test St'
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data

    def test_empty_address_validation(self, authenticated_client):
        """Test that empty address is rejected."""
        url = reverse('bank-list')
        data = {
            'name': 'Valid Bank',
            'type_bank': 'PRIVATE',
            'address': ''
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestBankAPI:
    """Tests for Bank API endpoints."""

    def test_list_banks(self, authenticated_client, bank):
        """Test listing banks."""
        url = reverse('bank-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_retrieve_bank(self, authenticated_client, bank):
        """Test retrieving a single bank."""
        url = reverse('bank-detail', kwargs={'pk': bank.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == bank.name

    def test_update_bank(self, authenticated_client, bank):
        """Test updating a bank."""
        url = reverse('bank-detail', kwargs={'pk': bank.pk})
        data = {'name': 'Updated Bank', 'type_bank': 'GOVERNMENT', 'address': bank.address}
        response = authenticated_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Bank'

    def test_delete_bank_soft_delete(self, authenticated_client, bank):
        """Test that delete performs soft delete."""
        url = reverse('bank-detail', kwargs={'pk': bank.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Bank should still exist but be soft deleted
        bank.refresh_from_db()
        assert bank.deleted_at is not None

    def test_unauthenticated_access(self, api_client):
        """Test that unauthenticated requests are rejected."""
        url = reverse('bank-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_filter_by_type(self, authenticated_client, bank):
        """Test filtering banks by type."""
        url = reverse('bank-list') + '?type_bank=PRIVATE'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_search_by_name(self, authenticated_client, bank):
        """Test searching banks by name."""
        url = reverse('bank-list') + '?search=Test'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
