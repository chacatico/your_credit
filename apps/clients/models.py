from django.db import models
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from apps.core.models import BaseModel

# Create your models here.
class Client(BaseModel):
    PERSON_TYPE_CHOICES = [
        ('INDIVIDUAL', 'Individual'),
        ('CORPORATE', 'Corporate'),
    ]

    full_name = models.CharField(max_length=150)
    birth_date = models.DateField()
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    nationality = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    person_type = models.CharField(max_length=20, choices=PERSON_TYPE_CHOICES)
    bank = models.ForeignKey('banks.Bank', on_delete=models.SET_NULL, null=True, blank=True, related_name='clients')

    def clean(self):
        # Validate age consistency
        if self.birth_date:
            today = date.today()
            calculated_age = today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
            if self.age != calculated_age:
                raise ValidationError({'age': f'The provided age ({self.age}) does not match the birth date ({calculated_age}).'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name