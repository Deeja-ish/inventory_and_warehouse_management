from .models import User
from rest_framework import serializers
from .models import Warehouse

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
        read_only_fields = ('warehouse_code', 'created_at', 'updated_at', 'is_active')

    # save the current serializer
    def __init__(self, *args, **kwags):
        super().__init__(*args, **kwags)
        # safetly get the request object
        request = self.context.get("request")

        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if 'manager' in self.fields:
                if not getattr(request.user, "is_system_admin", False):
                    self.fields['manager'].queryset = User.objects.filter(company=request.user.company, role=User.Role.MANAGER)
                else:
                    self.fields['manager'].queryset = User.objects.filter(role=User.Role.MANAGER)

    # validate the submitted request
    def validate(self, attrs):
        request = self.context.get('request')

        if request and not getattr(request.user, 'is_system_admin', False):
            company = attrs.get('company')

            # check if the company was provided
            if company and request.user.company !=company:
                raise serializers.ValidationError({'company' : "You cannot assign a warehouse"})

        return attrs

