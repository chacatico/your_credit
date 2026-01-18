import pytest
from datetime import date, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.clients.models import Client
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


@pytest.fixture
def client_data(bank):
    """Returns valid client data for testing."""
    today = date.today()
    birth_date = today.replace(year=today.year - 30)
    return {
        'full_name': 'John Doe',
        'birth_date': birth_date.isoformat(),
        'age': 30,
        'nationality': 'USA',
        'address': '456 Client Ave',
        'email': 'john@example.com',
        'phone': '+1234567890',
        'person_type': 'INDIVIDUAL',
        'bank': bank.pk
    }


@pytest.fixture
def client_instance(bank):
    today = date.today()
    birth_date = today.replace(year=today.year - 25)
    return Client.objects.create(
        full_name='Jane Doe',
        birth_date=birth_date,
        age=25,
        nationality='Canada',
        address='789 Test Blvd',
        email='jane@example.com',
        phone='+0987654321',
        person_type='INDIVIDUAL',
        bank=bank
    )


@pytest.mark.django_db
class TestClientModel:
    """Tests for Client model."""

    def test_client_creation(self, bank):
        """Test creating a client instance."""
        today = date.today()
        birth_date = today.replace(year=today.year - 35)
        client = Client.objects.create(
            full_name='Test Client',
            birth_date=birth_date,
            age=35,
            nationality='Mexico',
            address='Test Address',
            email='test@example.com',
            phone='1234567890',
            person_type='CORPORATE',
            bank=bank
        )
        assert client.full_name == 'Test Client'
        assert str(client) == 'Test Client'

    def test_client_soft_delete(self, client_instance):
        """Test soft delete functionality."""
        client_instance.soft_delete()
        assert client_instance.is_deleted is True
        assert client_instance.deleted_at is not None


@pytest.mark.django_db
class TestClientSerializer:
    """Tests for Client serializer validations."""

    def test_valid_client_data(self, authenticated_client, client_data):
        """Test creating client with valid data."""
        url = reverse('client-list')
        response = authenticated_client.post(url, client_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_age_mismatch_validation(self, authenticated_client, client_data):
        """Test that age inconsistent with birth_date is rejected."""
        client_data['age'] = 50  # Wrong age
        url = reverse('client-list')
        response = authenticated_client.post(url, client_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'age' in response.data

    def test_empty_name_validation(self, authenticated_client, client_data):
        """Test that empty name is rejected."""
        client_data['full_name'] = '   '
        url = reverse('client-list')
        response = authenticated_client.post(url, client_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_email_validation(self, authenticated_client, client_data):
        """Test that invalid email is rejected."""
        client_data['email'] = 'invalid-email'
        url = reverse('client-list')
        response = authenticated_client.post(url, client_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestClientAPI:
    """Tests for Client API endpoints."""

    def test_list_clients(self, authenticated_client, client_instance):
        """Test listing clients."""
        url = reverse('client-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_retrieve_client(self, authenticated_client, client_instance):
        """Test retrieving a single client."""
        url = reverse('client-detail', kwargs={'pk': client_instance.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['full_name'] == client_instance.full_name

    def test_delete_client_soft_delete(self, authenticated_client, client_instance):
        """Test that delete performs soft delete."""
        url = reverse('client-detail', kwargs={'pk': client_instance.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        client_instance.refresh_from_db()
        assert client_instance.deleted_at is not None

    def test_filter_by_person_type(self, authenticated_client, client_instance):
        """Test filtering clients by person type."""
        url = reverse('client-list') + '?person_type=INDIVIDUAL'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_search_by_name(self, authenticated_client, client_instance):
        """Test searching clients by name."""
        url = reverse('client-list') + '?search=Jane'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
