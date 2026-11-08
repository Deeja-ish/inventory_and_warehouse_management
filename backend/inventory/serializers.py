from .models import Category, Product, Inventory, StockTransaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction
from inventory.models import Warehouse

# create the category serializer
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'is_active', 'company')

    def create(self, validated_data):
        # create a request 
        request = self.context.get("request")
        # check it the request exists and the user is available
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['company'] = request.user.company

        return super().create(validated_data)

# create the product serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("created_at", 'updated_at', "is_active", "sku", "company")

    def __init__(self, *args, **kwags):
        super().__init__(*args, **kwags)

        request = self.context.get('request')
        # check the request and the user
        if request and hasattr(request, "user") and request.user.is_authenticated:
            if "category" in self.fields:
                if not getattr(request.user, "is_system_admin", False):
                    self.fields['category'].queryset = Category.objects.filter(company = request.user.company)
                else:
                    self.fields['category'].queryset = Category.objects.all()

    def create(self, validated_data):
        request = self.context.get("request")

        if request and hasattr(request, "user") and request.user.is_authenticated:
            if request.user.company is None:
                raise serializers.ValidationError({"company" : "No Company Provided"})
            validated_data['company'] = request.user.company
        return super().create(validated_data)


# create the stock transaction serializer
class StockTransactionSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = StockTransaction
        fields = "__all__"
        read_only_fields = ("quantity_before", "quantity_after", "created_at", "updated_at", "user")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            if not getattr(request.user, "is_system_admin", False):
                if "warehouse" in self.fields:
                    self.fields['warehouse'].queryset = Warehouse.objects.filter(company=request.user.company)
                if "product" in self.fields:
                    self.fields['product'].queryset = Product.objects.filter(company=request.user.company)

    def validate(self, attrs):
        request = self.context.get("request")
        if request and not getattr(request.user, "is_system_admin", False):
            warehouse = attrs.get('warehouse')
            product = attrs.get("product")

            if warehouse and product:
                if request.user.company != warehouse.company or request.user.company != product.company:
                    raise serializers.ValidationError({"error": "The warehouse or product provided does not belong to your company."})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get("request")
        product = validated_data['product']
        warehouse = validated_data['warehouse']
        transaction_type = validated_data['transaction_type']
        quantity = validated_data['quantity']
        reason = validated_data.get('reason', '')
        user = request.user

        # Lock the inventory row for update to prevent concurrent race conditions
        inventory = Inventory.objects.select_for_update().filter(product=product, warehouse=warehouse).first()

        # If inventory record does not exist yet:
        if inventory is None:
            if transaction_type in [StockTransaction.TransactionType.RECIEVE, StockTransaction.TransactionType.ADJUSTMENT]:
                inventory = Inventory.objects.create(
                    product=product,
                    warehouse=warehouse,
                    available_quantity=quantity
                )
                quantity_before = 0
                quantity_after = quantity
            else:
                raise serializers.ValidationError({
                    "transaction_type": f"Cannot perform '{transaction_type}' on non-existent inventory. You must Receive stock first."
                })
        else:
            quantity_before = inventory.available_quantity

            if transaction_type in [StockTransaction.TransactionType.RECIEVE, StockTransaction.TransactionType.RETURN]:
                quantity_after = quantity_before + quantity

            elif transaction_type == StockTransaction.TransactionType.ISSUE:
                if quantity > quantity_before:
                    raise serializers.ValidationError({
                        "quantity": f"Insufficient stock available. Current stock: {quantity_before}, Requested: {quantity}"
                    })
                quantity_after = quantity_before - quantity

            elif transaction_type == StockTransaction.TransactionType.ADJUSTMENT:
                # Target count adjustment
                quantity_after = quantity
            else:
                raise serializers.ValidationError({"transaction_type": "Invalid transaction type."})

            inventory.available_quantity = quantity_after
            inventory.save()

        # Record the transaction
        stock_transaction = StockTransaction.objects.create(
            product=product,
            warehouse=warehouse,
            user=user,
            transaction_type=transaction_type,
            quantity=quantity,
            quantity_before=quantity_before,
            quantity_after=quantity_after,
            reason=reason
        )

        return stock_transaction
            



# create the inventory serializer
class InventorySerializer(serializers.ModelSerializer):
    stock_status = serializers.SerializerMethodField()
    class Meta:
        model = Inventory
        fields = "__all__"
        read_only_fields = ("available_quantity", "reserved_quantity", "created_at", "updated_at", "is_active")

    # ensure the field avaliable belongs to the company
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            if not getattr(request.user, "is_system_admin", False):
                if 'warehouse' in self.fields:
                    self.fields['warehouse'].queryset = Warehouse.objects.filter(company= request.user.company)

                if 'product' in self.fields:
                    self.fields['product'].queryset = Product.objects.filter(company=request.user.company)

    # validate the user data 
    def validate(self, attrs):
        # validate the reorder level and minimu stock inventory 
        reorder_level = attrs.get("reorder_level", getattr(self.instance, "reorder_level", None))
        minimum_stock_level = attrs.get("minimum_quatity_level", getattr(self.instance, "minimum_quatity_level", None))

        if reorder_level is not None and minimum_stock_level is not None:
            if reorder_level <= minimum_stock_level:
                raise serializers.ValidationError({"message" : "Reoder level must be greater the Minimum Stock level"})

        # validate the product and the warehouse
        request = self.context.get("request")
        if request and not getattr(request.user, "is_system_admin", False):
            product = attrs.get("product")
            warehouse = attrs.get("warehouse")

            if (request and request.user.company != product.company) or (request.user.company != warehouse.company):
                raise serializers.ValidationError({"message" : "the user company and the product or warehouse company did not match"})
        return attrs

    # create a function to validate the stock status field 
    def get_stock_status(self, obj):
        available_quantity = obj.available_quantity or 0
        reorder_level = obj.reorder_level or 0
        minimum_stock_level = obj.minimum_quatity_level or 0

        if available_quantity <= minimum_stock_level:
            return "Critical"
        elif available_quantity <= reorder_level:
            return "Reorder"
        else:
            return "Normal"

        
        

    


