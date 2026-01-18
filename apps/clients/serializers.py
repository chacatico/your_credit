from datetime import date
from rest_framework import serializers
from apps.clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id', 'full_name', 'birth_date', 'age', 'nationality',
            'address', 'email', 'phone', 'person_type', 'bank',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_full_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Full name cannot be empty.")
        return value.strip()

    def validate_address(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Address cannot be empty.")
        return value.strip()

    def validate_nationality(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Nationality cannot be empty.")
        return value.strip()

    def validate_phone(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Phone cannot be empty.")
        return value.strip()

    def validate(self, attrs):
        """Cross-field validation for age consistency with birth_date."""
        birth_date = attrs.get('birth_date')
        age = attrs.get('age')

        if birth_date and age is not None:
            today = date.today()
            calculated_age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day)
            )
            if age != calculated_age:
                raise serializers.ValidationError({
                    'age': f'The provided age ({age}) does not match the birth date. Expected: {calculated_age}.'
                })

        return attrs
