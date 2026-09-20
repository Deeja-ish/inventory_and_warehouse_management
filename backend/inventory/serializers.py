from .models import Category, Product, Inventory, StockTransaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction

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
        read_only_fields = ("created_at", 'updated_at', "is_active", "sku")

    def __init__(self, *args, **kwags):
        super().__init__(*args, **kwags)

        request = self.context.get('request')
        # check the request and the user
        if request and hasattr(request, "user") and request.user.is_authenticated:
            if "company" in self.fields:
                self.fields['category'].queryset = Category.objects.filter(company = request.user.company)

        # validate the users data 
    def validate(self, attrs):
        request = self.context.get("request")
        # get the company
        if request:
            company = attrs.get('company')
        # compare the input and the companies
            if company and request.user.company != company:
                raise serializers.ValidationError({'company' : "The company assigned does not match the users company"})

        return attrs 


# create the stock transaction serializer
class StockTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransaction
        fields = "__all__"
        read_only_fields = ("quantity_before", "quantity_after", "created_at", "updated_at")

    @transaction.atomic
    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        warehouse = validated_data['warehouse']
        reason = validated_data['reason']
        transaction_type = validated_data['transaction_type']
        user = validated_data['user']

        try:
            inventory = Inventory.objects.filter(product=product, warehouse=warehouse).first()

            # check if the inventory does not exist 
            if inventory is None:
                if transaction_type == StockTransaction.TransactionType.RECIEVE and quantity > 0:
                    # get the current products quantity
                    add_inventory =Inventory.objects.create(
                        product = product,
                        warehouse = warehouse,
                        available_quantity = quantity
                    )
                    add_stock = StockTransaction.objects.create(
                        product = product,
                        warehouse = warehouse,
                        user= user,
                        quantity_before = 0,
                        quantity_after = quantity,
                        quantity=quantity,
                        transaction_type = transaction_type,
                        reason = reason
                    )

                    return add_inventory, add_stock

                else:
                    raise ValidationError("Inventory does not exist for the given product and warehouse.")

            # check if transaction type and inventory exist 
            if inventory is not None:
                if transaction_type in [StockTransaction.TransactionType.RECIEVE, StockTransaction.TransactionType.RETURN] and quantity > 0:
                    current_quantity = inventory.available_quantity
                    quantity_before = current_quantity
                    quantity_after = quantity_before + quantity

                    inventory.available_quantity = quantity_after
                    inventory.save()

                    new_transaction = StockTransaction.objects.create(
                        product = product,
                        warehouse = warehouse,
                        user = user,
                        transaction_type = transaction_type,
                        quantity_before = quantity_before,
                        quantity_after = quantity_after,
                        quantity = quantity,
                        reason = reason
                    )

                    return new_transaction
            
                elif transaction_type == StockTransaction.TransactionType.ISSUE and quantity > 0:
                    current_quantity_issue = inventory.available_quantity
                    quantity_before_issue = current_quantity_issue

                    # check if available stock is enough for issue
                    if quantity > quantity_before_issue:
                        raise ValidationError("Insufficient stock available")
                    
                    quantity_after_issue = quantity_before_issue - quantity

                    inventory.available_quantity = quantity_after_issue
                    inventory.save()

                    new_transaction_issue = StockTransaction.objects.create(
                        product = product,
                        warehouse = warehouse,
                        user = user,
                        transaction_type = transaction_type,
                        quantity_before = quantity_before_issue,
                        quantity = quantity,
                        quantity_after = quantity_after_issue,
                        reason = reason
                    )

                    return new_transaction_issue
                
                elif transaction_type == StockTransaction.TransactionType.ADJUSTMENT and quantity > 0:
                    # the current quantity
                    current_quantity_adjustment = inventory.available_quantity
                    quantity_before_adjustment= current_quantity_adjustment
                    # the quantity level after return
                    quantity_after_adjustment = quantity 

                    inventory.available_quantity = quantity_after_adjustment 
                    inventory.save()

                    # update a transaction 
                    new_transaction_adjustment = StockTransaction.objects.create(
                        product= product,
                        warehouse=warehouse,
                        user=user,
                        transaction_type = transaction_type,
                        quantity_before = quantity_before_adjustment,
                        quantity_after = quantity_after_adjustment,
                        quantity =quantity,
                        reason = reason 
                    )

                    return new_transaction_adjustment
                raise ValidationError("Invalid transaction type or quantity for stock")

        except Exception as e:
            raise ValidationError(f"Error processing stock transaction: {str(e)}")



# create the inventory serializer
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"
        read_only_fields = ("product", "warehouse", "available_quantity", "reserved_quantity", "created_at", "updated_at", "is_active")

    


