from .models import User
from rest_framework import serializers

# create a user serialiser
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['employee_ID', 'username', 'password', 'confirm_password','first_name', 'last_name', 'email', 'company', 'role', 'is_system_admin']

        read_only_fields = ['employee_ID', 'is_active', 'created_at', 'updated_at']

        # validate the password
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"password" : "passwords do not match"})
        return attrs

    # create the new user with the password
    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("confirm_password")

        # save the user 
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


