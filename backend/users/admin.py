from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):

    # the fields to display
    list_display = ("employee_ID", "username", "email", "first_name", "last_name", "company", "role", "is_active")

    # the fields to filter
    list_filter = UserAdmin.list_filter + ("role", "company", "is_active")

    # fields ypu can search
    search_fields = ("employee_ID", "username", "email")

    


