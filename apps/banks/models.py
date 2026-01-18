from django.db import models
from apps.core.models import BaseModel

# Create your models here.
class Bank(BaseModel):
    TYPE_CHOICES = [
        ('PRIVATE', 'Private'),
        ('GOVERNMENT', 'Government'),
    ]

    name = models.CharField(max_length=100)
    type_bank = models.CharField(max_length=20, choices=TYPE_CHOICES)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name