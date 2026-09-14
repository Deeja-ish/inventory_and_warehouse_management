from django.contrib import admin
from .models import Category, Inventory, Product, StockTransaction

# Register your models here.
@admin.register(Category)
class CustomCategory(admin.ModelAdmin):
    list_display = ("category_name", "category_description", "is_active")

    list_filter = ("is_active",)

    search_fields = ("category_name",)

@admin.register(Product)
class CustomProduct(admin.ModelAdmin):
    list_display = ("company", "category", "product_name", "product_description", "sku", "product_type", "unit_of_measure", "reorder_level", "is_active", "created_at")

    list_filter = ("company", "category", "product_type", "unit_of_measure", "is_active", "product_name", "sku")

    search_fields = ("company__company_name", "category__category_name", "product_type")

@admin.register(Inventory)
class CustomInventory(admin.ModelAdmin):
    list_display = ("product", "warehouse", "available_quantity", "reserved_quantity", "is_active")

    list_filter = ("product", "warehouse")

    search_fields = ("product__product_name", "warehouse__warehouse_name")

@admin.register(StockTransaction)
class CustomTransaction(admin.ModelAdmin):
    list_display= ("product", "warehouse", "user", "quantity", "quantity_before", "quantity_after", "transaction_type", "reason")

    list_filter = ("product", "warehouse", "transaction_type", "user")

    search_fields = ("product__product_name", "warehouse__warehouse_name", "user__role", "user__employee_ID", "user__")

