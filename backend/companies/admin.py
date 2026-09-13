from django.contrib import admin
from .models import Company

# Register your models here.
@admin.register(Company)
class CustomCompanyView(admin.ModelAdmin):

    list_display = ("company_name", "registration_number", "email", "phone_number", "created_at", "is_active")

    list_filter = ('is_active', "created_at")

    search_fields  = ("company_name", "registration_number", "email")



