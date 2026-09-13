from django.db import models
from companies.models import Company
from users.models import User
import uuid

# Create your models here.
class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=100)
    warehouse_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50)
    address = models.TextField(max_length=200)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='warehouses')
    class WarehouseType(models.TextChoices):
        RAW_MATERIAL = "Raw_materials", "RAW_MATERIALS", "raw_materials"
        PACKING_MATERIAL = "Packing_materials", "PACKING_MATRIALS", "packing_materials"
        FINISHED_GOODS = "Finished_goods", "FINISHED_GOODS", "finished_goods"
        COLD_STORAGE = "Cold_storage", "COLD_STORAGE", "cold_storage"
        DAMAGED = "Damaged", "DAMAGED", "damaged"
        CHEMICAL_STORAGE = "Chemical_storage", "CHEMICAL_STORAGE", "chemical_storage"
        DISTRIBUTION_CENTER = "Distribution_center", "DISTRIBUTION_CENTER", "distribution_center"
    warehouse_type = models.CharField(max_length=100, choices=WarehouseType.choices)
    is_active = models.BooleanField(default=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='warehouse_manager')
    capacity = models.DecimalField(max_length=100, blank=True, null=True)
    capacity_unit = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.warehouse_code:
            unique_code = str(uuid.uuid3())[:4].upper()
            self.warehouse_code = f"WH-{unique_code}"

            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.warehouse_name} -{self.warehouse_type} - {self.warehouse_code}"