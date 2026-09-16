import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from companies.models import Company

# Create your models here.
# creating the user model from the abstract user
class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    employee_ID = models.CharField(max_length=20, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='users', null=True)
    class Role(models.TextChoices):
        ADMIN = "Admin", "ADMIN"
        MANAGER = "Manager", "MANAGER"
        STORE_KEEPER = "Store_keeper", "STORE_KEEPER"
        AUDITOR = "Auditor", "AUDITOR"
    role = models.CharField(max_length=20, choices=Role.choices)
    is_system_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.employee_ID:
            # generate a random number string
            unique_string = str(uuid.uuid4())[:8].upper()
            self.employee_ID = f"EMP-{unique_string}"

        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.employee_ID} - {self.email}"


