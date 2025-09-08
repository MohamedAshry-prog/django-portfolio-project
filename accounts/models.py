from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    USER_ROLES = (
        ('ADMIN', 'مسؤول النظام'),
        ('GENERAL_MANAGER', 'مدير عام الإدارة'),
        ('DEPARTMENT_MANAGER', 'مدير الإدارة'),
        ('EMPLOYEE', 'موظف'),
    )
    id = models.SmallAutoField(primary_key=True)
    role = models.CharField(max_length=20, choices=USER_ROLES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    
