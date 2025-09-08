from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from tasks.models import Task
from django.db.models import Count, Q
from accounts.models import User, Department
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def employee_dashboard(request):
    user = request.user
    tasks = Task.objects.filter(created_by=user)
    
    # إحصائيات المهام
    stats = {
        'total': tasks.count(),
        'completed': tasks.filter(status='COMPLETED').count(),
        'in_progress': tasks.filter(status='IN_PROGRESS').count(),
        'pending': tasks.filter(status='PENDING').count(),
        'cancelled': tasks.filter(status='CANCELLED').count(),
    }
    
    # المهام المضافة حديثاً
    
    
        
    return render(request, 'reports/employee_dashboard.html', {
        'stats': stats,
        'tasks': tasks,
        
    })

@login_required
def department_dashboard(request):
    # Authorization check
    if not request.user.is_authenticated or request.user.role not in ['DEPARTMENT_MANAGER', 'GENERAL_MANAGER', 'ADMIN']:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    # Determine department - general managers can view any department
    department = request.user.department
    
    # If general manager or admin, allow department selection
    if request.user.role in ['GENERAL_MANAGER', 'ADMIN'] and 'department_id' in request.GET:
        try:
            department = Department.objects.get(pk=request.GET.get('department_id'))
        except Department.DoesNotExist:
            pass  # Fall back to user's own department
    
    # Get all departments for selector (for general managers/admins)
    all_departments = Department.objects.all() if request.user.role in ['GENERAL_MANAGER', 'ADMIN'] else None
    
    # Department tasks statistics
    department_stats = {
        'total_tasks': Task.objects.filter(assigned_to__department=department).count(),
        'completed_tasks': Task.objects.filter(
            assigned_to__department=department,
            status='COMPLETED'
        ).count(),
        'in_progress_tasks': Task.objects.filter(
            assigned_to__department=department,
            status='IN_PROGRESS'
        ).count(),
        'pending_tasks': Task.objects.filter(
            assigned_to__department=department,
            status='PENDING'
        ).count(),
    }
    
    # Employee statistics within the department
    employee_stats = User.objects.filter(department=department).annotate(
        total_tasks=Count('created_tasks'),
        completed_tasks=Count('created_tasks', filter=Q(created_tasks__status='COMPLETED')),
        in_progress_tasks=Count('created_tasks', filter=Q(created_tasks__status='IN_PROGRESS')),
        pending_tasks=Count('created_tasks', filter=Q(created_tasks__status='PENDING')),
    ).order_by('-completed_tasks')  # Sort by most productive
    
    return render(request, 'reports/department_dashboard.html', {
        'employee_stats': employee_stats,
        'department': department,
        'department_stats': department_stats,
        'all_departments': all_departments,  # For general manager's department selector
        'is_general_manager': request.user.role in ['GENERAL_MANAGER', 'ADMIN'],
    })

@login_required
def general_dashboard(request):
    # Check authorization
    if not request.user.is_authenticated or request.user.role not in ['GENERAL_MANAGER', 'ADMIN']:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    # Get all departments (not just the first one)
    departments = Department.objects.all().annotate(
        total_users=Count('user', distinct=True),
        total_tasks=Count('user__assigned_tasks', distinct=True),
        completed_tasks=Count(
            'user__assigned_tasks',
            filter=Q(user__assigned_tasks__status='COMPLETED'),
            distinct=True
        ),
        in_progress_tasks=Count(
            'user__assigned_tasks',
            filter=Q(user__assigned_tasks__status='IN_PROGRESS'),
            distinct=True
        ),
        pending_tasks=Count(
            'user__assigned_tasks',
            filter=Q(user__assigned_tasks__status='PENDING'),
            distinct=True
        ),
    )
    
    # Calculate overall statistics
    overall_stats = {
        'total_departments': departments.count(),
        'total_users': sum(dept.total_users for dept in departments),
        'total_tasks': sum(dept.total_tasks for dept in departments),
        'completed_tasks': sum(dept.completed_tasks for dept in departments),
        'completion_rate': round(
            sum(dept.completed_tasks for dept in departments) / 
            max(1, sum(dept.total_tasks for dept in departments)) * 100,
            2
        ) if departments else 0,
    }
    
    tasks_total_based_on_type = Task.objects.all().aggregate(
        total_tasks=Count('task_pk'),
        completed_tasks=Count('task_pk', filter=Q(status='COMPLETED')),
        in_progress_tasks=Count('task_pk', filter=Q(status='IN_PROGRESS')),
        pending_tasks=Count('task_pk', filter=Q(status='PENDING')),
    )
    
    return render(request, 'reports/general_dashboard.html', {
        'departments': departments,
        'overall_stats': overall_stats,
        'total': tasks_total_based_on_type,
    })


@login_required
def filter_tasks(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    try:
        date_from = timezone.datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = timezone.datetime.strptime(date_to, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return JsonResponse({'error': 'صيغة التاريخ غير صحيحة'}, status=400)
    
    if request.user.role == 'EMPLOYEE':
        tasks = Task.objects.filter(
            assigned_to=request.user,
            created_at__date__range=[date_from, date_to]
        )
    elif request.user.role == 'DEPARTMENT_MANAGER':
        tasks = Task.objects.filter(
            assigned_to__department=request.user.department,
            created_at__date__range=[date_from, date_to]
        )
    else:
        tasks = Task.objects.filter(
            created_at__date__range=[date_from, date_to]
        )
    
    # يمكن إرجاع البيانات كـ JSON أو عرضها في قالب
    data = {
        'tasks': [
            {
                'title': task.title,
                'status': task.get_status_display(),
                'assigned_to': task.assigned_to.get_full_name(),
                'created_at': task.created_at.strftime('%Y-%m-%d')
            }
            for task in tasks
        ]
    }
    
    return JsonResponse(data)


@login_required
def task_details(request, task_id):
    task = Task.objects.filter(pk=task_id)
    
    return render(request, 'reports/task_overview.html', {
        'task': task,
    })