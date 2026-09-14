from django.contrib import admin
from .models import Warehouse
# Register your models here.

@admin.register(Warehouse)
class CustomWarehouse(admin.ModelAdmin):
    list_display = ("warehouse_name", "warehouse_code", "warehouse_type", "state", "country", "company", "manager", "is_active",  "capacity", "created_at")

    list_filter = ("is_active", "warehouse_type", "capacity_unit", "state", "company")

    search_fields = ("warehouse_code", "warehouse_type", "state", "company__company_name", "warehouse_name", "manager__employee_ID")