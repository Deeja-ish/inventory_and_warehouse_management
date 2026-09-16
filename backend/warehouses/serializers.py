from rest_framework import serializers
from .models import Warehouse

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
        read_only_fields = ('warehouse_code', 'created_at', 'updated_at', 'is_active')

    def validate(self, attrs):
        # to check if the warehouse belongs to the company the manager is tryng to access 
        if self.request.user.company != attrs.get('company'):
            raise serializers.ValidationError({"company": "you can not access this company"})
        return attrs

