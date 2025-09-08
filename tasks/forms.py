from django.forms import ModelForm, forms
from .models import Task

from django import forms
from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        # لا نعرض الحقول التي نعينها من view
        exclude = ['created_by', 'assigned_to', 'task_pk', 'created_at', 'updated_at', 'completion_notes']
        widgets = {
            'date_mission': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'Scope_of_work': forms.TextInput(attrs={'class': 'form-control'}),
            'time_duration': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'Important_periodicity': forms.Select(attrs={'class': 'form-control'}),
            'time_duration_unit': forms.Select(attrs={'class': 'form-control'}),
            'important_degree': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
