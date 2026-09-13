from django.db import models

# Create your models here.
class Company(models.Model):
    company_name = models.CharField(max_length=100, unique=True)
    registration_number = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=True, max_length=50)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.registration_number}"

