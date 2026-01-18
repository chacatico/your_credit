from rest_framework import serializers
from apps.banks.models import Bank


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'name', 'type_bank', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Bank name cannot be empty.")
        return value.strip()

    def validate_address(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Address cannot be empty.")
        return value.strip()
