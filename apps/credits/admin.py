from django.contrib import admin
from apps.credits.models import Credit

# Register your models here.
@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('credit_type', 'client', 'bank', 'term_months', 'registration_date')
    search_fields = ('client__full_name', 'description')
    list_filter = ('credit_type', 'bank', 'registration_date')
    autocomplete_fields = ['client', 'bank']