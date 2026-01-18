from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from apps.core.models import BaseModel

# Create your models here.
class Credit(BaseModel):
    CREDIT_TYPE_CHOICES = [
        ('AUTOMOTIVE', 'Automotive'),
        ('MORTGAGE', 'Mortgage'),
        ('COMMERCIAL', 'Commercial'),
    ]

    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='credits')
    description = models.CharField(max_length=255)
    minimum_payment = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    maximum_payment = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    term_months = models.PositiveIntegerField()
    registration_date = models.DateTimeField(auto_now_add=True)
    bank = models.ForeignKey('banks.Bank', on_delete=models.CASCADE, related_name='credits')
    credit_type = models.CharField(max_length=20, choices=CREDIT_TYPE_CHOICES)

    def clean(self):
        if self.minimum_payment is not None and self.maximum_payment is not None:
            if self.minimum_payment > self.maximum_payment:
                raise ValidationError({'minimum_payment': 'Minimum payment cannot be greater than maximum payment.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.credit_type} - {self.client}"
