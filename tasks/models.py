from django.db import models
from accounts.models import User
import uuid
class Task(models.Model):
    TASK_STATUS = (
        ('PENDING', 'قيد الانتظار'),
        ('IN_PROGRESS', 'قيد التنفيذ'),
        ('COMPLETED', 'مكتمل'),
        ('CANCELLED', 'ملغى'),
    )
    task_pk = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    important_degree = models.CharField(max_length=20,null=True, choices=[('important', 'هام'), ('Very_important', 'هام جداً'),], default='important')
    Scope_of_work = models.CharField(max_length=200, null=True, blank=True)
    date_mission = models.DateField()
    time_duration = models.IntegerField()
    time_duration_unit = models.CharField(max_length=20, choices=[('hours', 'ساعات'), ('days', 'أيام'), ('weeks', 'أسابيع')], default='days')
    Important_periodicity = models.CharField(max_length=20, null=True, choices=[('daily', 'يومي'), ('weekly', 'أسبوعي'), ('monthly', 'شهري')], default='daily')
    status = models.CharField(max_length=20, choices=TASK_STATUS, default='PENDING')
    completion_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"