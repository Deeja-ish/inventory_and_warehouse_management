from .models import User
from rest_framework import serializers
from .models import Warehouse
from companies.models import Company
class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
        read_only_fields = ('warehouse_code', 'created_at', 'updated_at', 'is_active', 'company')

    # save the current serializer
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # safetly get the request object
        request = self.context.get("request")

        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if 'manager' in self.fields:
                if not getattr(request.user, "is_system_admin", False):
                    self.fields['manager'].queryset = User.objects.filter(company=request.user.company, role=User.Role.MANAGER)
                else:
                    self.fields['manager'].queryset = User.objects.filter(role=User.Role.MANAGER)

    def create(self, validated_data):
        request = self.context.get("request")

        if request and hasattr(request, "user") and request.user.is_authenticated:
            if request.user.company is None:
                raise serializers.ValidationError({"company" : "No Company Provided."})
            validated_data['company'] = request.user.company

        return super().create(validated_data)
