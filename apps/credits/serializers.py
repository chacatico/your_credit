from rest_framework import serializers
from apps.credits.models import Credit
from apps.banks.serializers import BankSerializer


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = [
            'id', 'client', 'description', 'minimum_payment', 'maximum_payment',
            'term_months', 'registration_date', 'bank', 'credit_type',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'registration_date', 'created_at', 'updated_at']

    def validate_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        return value.strip()

    def validate_term_months(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Term months must be greater than zero.")
        return value

    def validate(self, attrs):
        """Cross-field validation: minimum_payment <= maximum_payment."""
        minimum_payment = attrs.get('minimum_payment')
        maximum_payment = attrs.get('maximum_payment')

        if minimum_payment is not None and maximum_payment is not None:
            if minimum_payment > maximum_payment:
                raise serializers.ValidationError({
                    'minimum_payment': 'Minimum payment cannot be greater than maximum payment.'
                })

        return attrs


class CreditWithBankSerializer(serializers.ModelSerializer):
    """Credit serializer with nested bank details for read operations."""
    bank = BankSerializer(read_only=True)

    class Meta:
        model = Credit
        fields = [
            'id', 'description', 'minimum_payment', 'maximum_payment',
            'term_months', 'registration_date', 'bank', 'credit_type',
            'created_at', 'updated_at'
        ]
