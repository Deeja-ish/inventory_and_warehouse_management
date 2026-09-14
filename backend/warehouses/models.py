from django.db import models
from companies.models import Company
from users.models import User

# Create your models here.
class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=100)
    warehouse_code = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    address = models.TextField(max_length=200)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='warehouses')
    class WarehouseType(models.TextChoices):
        RAW_MATERIAL = "Raw_materials", "RAW_MATERIALS"
        PACKING_MATERIAL = "Packing_materials", "PACKING_MATERIALS"
        FINISHED_GOODS = "Finished_goods", "FINISHED_GOODS"
        COLD_STORAGE = "Cold_storage", "COLD_STORAGE"
        DAMAGED = "Damaged", "DAMAGED"
        CHEMICAL_STORAGE = "Chemical_storage", "CHEMICAL_STORAGE"
        DISTRIBUTION_CENTER = "Distribution_center", "DISTRIBUTION_CENTER"
    warehouse_type = models.CharField(max_length=100, choices=WarehouseType.choices)
    is_active = models.BooleanField(default=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='warehouse_manager')
    capacity = models.PositiveIntegerField(blank=True, null=True)
    class CapacityUnit(models.TextChoices):
        PALLETS = "Pallets", "PALLETS"
        CARTONS = "Carton", "CARTON"
        BOXES = "Boxes", "BOXES"
        KILOGRAM = "Kilogram", 'KG'
        LITERS = "Liters", "LITERS" 
    capacity_unit = models.CharField(max_length=50, choices=CapacityUnit.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'warehouse_name'], name="unique_company_warehouse_type"), 
            models.UniqueConstraint(fields=['company', 'warehouse_code'], name='unique_company_warehouse_code'),
        ]
        ordering = ['company', "warehouse_name"]

    
    def save(self, *args, **kwargs):
        if not self.warehouse_code:
            initials = {
                self.WarehouseType.RAW_MATERIAL: "RM",
                self.WarehouseType.PACKING_MATERIAL: "PM",
                self.WarehouseType.FINISHED_GOODS: "FG",
                self.WarehouseType.COLD_STORAGE: "CS",
                self.WarehouseType.DAMAGED: "DM",
                self.WarehouseType.CHEMICAL_STORAGE: "CH",
                self.WarehouseType.DISTRIBUTION_CENTER: "DC",
            }

            initial = initials[self.warehouse_type]
            # count the existing warehouse and add one 
            current_count = Warehouse.objects.filter(company=self.company, warehouse_type=self.warehouse_type).count()

            # sequence_number 
            sequence_number = str(current_count + 1).zfill(3)
            # write the code
            self.warehouse_code = f"WH-{initial}-{sequence_number}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.warehouse_name} -{self.warehouse_type} - {self.warehouse_code}"