from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# create a user serialiser
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id", 'employee_ID', 'username', 'password', 'confirm_password','first_name', 'last_name', 'email', 'company', 'role', "is_system_admin"]

        read_only_fields = ['employee_ID', 'is_active', 'role', 'is_system_admin']

        extra_kwargs = {"company" : {"required" : True, "allow_null" : False}}

        # validate the password
    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if self.instance is None and not password:
            raise serializers.ValidationError({"message" : "Password is required"})

        if password is not None or confirm_password is not None:
            if password != confirm_password:
                raise serializers.ValidationError({"message" : "Passwords must ne similar"})
        
            candidate = self.instance or User(
                first_name=attrs.get("first_name"), last_name=attrs.get("last_name"), 
                email = attrs.get("email"), username=attrs.get("username")
            )

            try:
                validate_password(password, candidate)
            except ValidationError as e:
                raise serializers.ValidationError({"password" : list(e.messages)})

        request = self.context.get("request")
        if self.instance and 'company' in attrs and attrs['company'] != self.instance.company:
            if not(request and getattr(request.user, 'is_system_admin', False)):
                raise serializers.ValidationError({"company" : "You cannot change a users company"})       

        return attrs 

    # create the new user with the password
    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("confirm_password")
        # check for an admin in a company
        company = validated_data['company']
        first_user = not company.users.exists()
        validated_data["role"] = User.Role.ADMIN if first_user else User.Role.STAFF   
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

    # update the password and store it.
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        confirm_password = validated_data.pop("confirm_password", None)

        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user 

class UserDisplayProfileView(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name","employee_ID", "company", "role", "is_system_admin"]

# make a change password serialiser
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        request = self.context.get("request")
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user 
        else:
            raise serializers.ValidationError("User must be authenticated")
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
            # check if the old password is required 
        if not user.check_password(old_password):
            raise serializers.ValidationError({"passwords" : "Old Password is incorrect"})
            # check if old password is correct
        if old_password == new_password:
            raise serializers.ValidationError({"new_password" : "New password mst differ from old password "})

        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            raise serializers.ValidationError({'password' : list(e.messages)})
        return attrs

# create logout serializer 
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    def validate(self, attrs):
        self.token = attrs.get("refresh")
        return attrs

    def save(self, **kwargs):
        try:
            token_obj = RefreshToken(self.token)
            token_obj.blacklist()
        except TokenError:
            raise serializers.ValidationError({"Token" : "Token has expired or is not valid"})


# a serialiser to show user