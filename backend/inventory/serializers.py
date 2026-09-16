from .models import Category, Product, Inventory, StockTransaction
from rest_framework import serializers

# create the category serializer
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'is_active')


# create the product serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("created_at", 'updated_at', "is_active", "product_code")