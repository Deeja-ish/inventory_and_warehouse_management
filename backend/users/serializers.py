from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

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


class UserDisplayProfileView(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name","employee_ID", "company", "role", "is_system_admin")

# make a change password serialiser
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        request = self.context.get("request")
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user 
            old_password = attrs.get("old_password")
            new_password = attrs.get("new_password")
            # check if the old password is required 
            if not user.check_password(old_password):
                raise serializers.ValidationError({"passwords" : "Old Password is required"})
            # check if old password is correct
            if user.check_password(new_password):
                raise serializers.ValidationError({"password" : "new and old passwords cannot be the same"})
        return attrs

# create logout serializer 
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    def validate(self, attrs):
        self.token = attrs.get("refresh")
        return attrs

    def save(self, **kwags):
        try:
            token_obj = RefreshToken(self.token)
            token_obj.blacklist()
        except TokenError:
            raise serializers.ValidationError({"Token" : "Token has expired or is not valid"})

        