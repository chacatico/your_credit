from django.contrib import admin
from apps.banks.models import Bank

# Register your models here.
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_bank', 'address')
    search_fields = ('name',)
    list_filter = ('type_bank',)