import pytest
from datetime import date
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.credits.models import Credit
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
def client_instance(bank):
    today = date.today()
    birth_date = today.replace(year=today.year - 30)
    return Client.objects.create(
        full_name='Test Client',
        birth_date=birth_date,
        age=30,
        nationality='USA',
        address='456 Client Ave',
        email='test@example.com',
        phone='+1234567890',
        person_type='INDIVIDUAL',
        bank=bank
    )


@pytest.fixture
def credit_instance(client_instance, bank):
    return Credit.objects.create(
        client=client_instance,
        description='Home Loan',
        minimum_payment=Decimal('500.00'),
        maximum_payment=Decimal('2000.00'),
        term_months=36,
        bank=bank,
        credit_type='MORTGAGE'
    )


@pytest.fixture
def credit_data(client_instance, bank):
    return {
        'client': client_instance.pk,
        'description': 'Car Loan',
        'minimum_payment': '300.00',
        'maximum_payment': '1500.00',
        'term_months': 24,
        'bank': bank.pk,
        'credit_type': 'AUTOMOTIVE'
    }


@pytest.mark.django_db
class TestCreditModel:
    """Tests for Credit model."""

    def test_credit_creation(self, client_instance, bank):
        """Test creating a credit instance."""
        credit = Credit.objects.create(
            client=client_instance,
            description='Business Loan',
            minimum_payment=Decimal('1000.00'),
            maximum_payment=Decimal('5000.00'),
            term_months=48,
            bank=bank,
            credit_type='COMMERCIAL'
        )
        assert credit.description == 'Business Loan'
        assert credit.term_months == 48

    def test_credit_str(self, credit_instance):
        """Test credit string representation."""
        assert 'MORTGAGE' in str(credit_instance)

    def test_credit_soft_delete(self, credit_instance):
        """Test soft delete functionality."""
        credit_instance.soft_delete()
        assert credit_instance.is_deleted is True
        assert credit_instance.deleted_at is not None


@pytest.mark.django_db
class TestCreditSerializer:
    """Tests for Credit serializer validations."""

    def test_valid_credit_data(self, authenticated_client, credit_data):
        """Test creating credit with valid data."""
        url = reverse('credit-list')
        response = authenticated_client.post(url, credit_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_min_greater_than_max_validation(self, authenticated_client, credit_data):
        """Test that minimum_payment > maximum_payment is rejected."""
        credit_data['minimum_payment'] = '5000.00'
        credit_data['maximum_payment'] = '1000.00'
        url = reverse('credit-list')
        response = authenticated_client.post(url, credit_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'minimum_payment' in response.data

    def test_empty_description_validation(self, authenticated_client, credit_data):
        """Test that empty description is rejected."""
        credit_data['description'] = '   '
        url = reverse('credit-list')
        response = authenticated_client.post(url, credit_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_zero_term_validation(self, authenticated_client, credit_data):
        """Test that zero term_months is rejected."""
        credit_data['term_months'] = 0
        url = reverse('credit-list')
        response = authenticated_client.post(url, credit_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCreditAPI:
    """Tests for Credit API endpoints."""

    def test_list_credits(self, authenticated_client, credit_instance):
        """Test listing credits."""
        url = reverse('credit-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_retrieve_credit(self, authenticated_client, credit_instance):
        """Test retrieving a single credit."""
        url = reverse('credit-detail', kwargs={'pk': credit_instance.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['description'] == credit_instance.description

    def test_update_credit(self, authenticated_client, credit_instance):
        """Test updating a credit."""
        url = reverse('credit-detail', kwargs={'pk': credit_instance.pk})
        data = {
            'client': credit_instance.client.pk,
            'description': 'Updated Loan',
            'minimum_payment': '600.00',
            'maximum_payment': '2500.00',
            'term_months': 48,
            'bank': credit_instance.bank.pk,
            'credit_type': 'MORTGAGE'
        }
        response = authenticated_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['description'] == 'Updated Loan'

    def test_delete_credit_soft_delete(self, authenticated_client, credit_instance):
        """Test that delete performs soft delete."""
        url = reverse('credit-detail', kwargs={'pk': credit_instance.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        credit_instance.refresh_from_db()
        assert credit_instance.deleted_at is not None

    def test_filter_by_credit_type(self, authenticated_client, credit_instance):
        """Test filtering credits by type."""
        url = reverse('credit-list') + '?credit_type=MORTGAGE'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_search_by_description(self, authenticated_client, credit_instance):
        """Test searching credits by description."""
        url = reverse('credit-list') + '?search=Home'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
