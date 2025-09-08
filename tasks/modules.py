from .models import (
    Task,
    User,
)
from django.db.models import Count

def count_tasks_by_status(request):
    total = Task.objects.filter(assigned_to=5).count()
    print(total)
    
    return {
        'PENDING': Task.objects.filter(created_by=request.user.id, status='PENDING').count(),
        'IN_PROGRESS': (Task.objects.filter(created_by=request.user.id, status='IN_PROGRESS').count()+
                        Task.objects.filter(created_by=request.user.id, status='CANCELLED').count()),
        'COMPLETED': Task.objects.filter(created_by=request.user.id, status='COMPLETED').count(),
        'total': Task.objects.filter(created_by=request.user.id).count(),
    }