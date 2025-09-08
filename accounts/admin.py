from django.contrib import admin
from .models import Department, User

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # إزالة created_at
    ordering = ('name',)  # إزالة created_at
    search_fields = ('name',)

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_full_name', 'role', 'department')
    list_filter = ('role', 'department')
    search_fields = ('username', 'email', 'first_name', 'last_name')