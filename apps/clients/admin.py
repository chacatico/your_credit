from django.contrib import admin
from apps.clients.models import Client
from apps.banks.models import Bank

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'person_type', 'email', 'phone')
    search_fields = ('full_name', 'email', 'phone')
    list_filter = ('person_type', 'bank')