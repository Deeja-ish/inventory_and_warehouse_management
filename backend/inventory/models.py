from django.db import models
from companies.models import Company
from warehouses.models import Warehouse
from users.models import User

# Create your models here.

# creating the category model
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category_name}"

# build the product model
class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="products") 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products_category')
    product_name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, blank=True, null=True)
    class ProductType(models.TextChoices):
        RAW_MATERIAL = "Raw_materials", "raw_materials"
        FINISHED_GOODS = "Finished_goods", "finished_goods"
        PACKING_MATERIAL = "Packing_materials", "packing_materials"
        CONSUMABLE = "Consumable", "consumable"
    product_type = models.CharField(max_length=100, choices=ProductType.choices)
    class UnitType(models.TextChoices):
        KG = "KG", "Kilogram"
        LITER = "L", "Liter"
        PIECE = "PCS", "Pieces"
        BOX = "BOX", "Boxes"
        CARTON = "CTN", "Cartons"
        PACK = "PACK", "Packs"
    unit_of_measure = models.CharField(max_length=50, choices=UnitType.choices)
    product_description = models.TextField(blank=True)
    reorder_level = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', "product_name"], name="unique_company_product_name"),
            models.UniqueConstraint(fields=['company', 'sku'], name='unique_company_sku_name')
        ]

        ordering = ["company", "product_name"]

    def save(self, *args, **kwags):
        if not self.sku:

            # get the intials of the product type 
            initials = {
                self.ProductType.RAW_MATERIAL : "RM",
                self.ProductType.FINISHED_GOODS : "FG",
                self.ProductType.PACKING_MATERIAL : "PM",
                self.ProductType.CONSUMABLE : "CM"
            }

            intial = initials[self.product_type]
            # count the products base on unique company
            unique_count = Product.objects.filter(company=self.company, product_type=self.product_type).count()
            count = str(unique_count + 1).zfill(3)

            self.sku = f"{intial}-{count}"

        super().save(*args, **kwags)


    def __str__(self):
        return f"{self.product_name} - {self.company} - {self.product_type}"



# create the inventory model 
class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_product')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventory_warehouse')
    available_quantity = models.PositiveIntegerField()
    reserved_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} - {self.available_quantity} - {self.warehouse}"

# creating the stock transaction model 
class StockTransaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_product')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_warehouse')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stock_user')
    class TransactionType(models.TextChoices):
        RECIEVE = "Received", "received" 
        ISSUE = "Issue", "issue"
        RETURN = "Return", "return"
        ADJUSTMENT = "Adjustment", "adjustment"
    transaction_type = models.CharField(max_length=50, choices=TransactionType.choices)
    quantity_before = models.IntegerField(default=0)
    quantity_after = models.IntegerField()
    quantity = models.IntegerField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product}-{self.quantity}-{self.quantity_unit}-{self.user}"
