from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from tasks.forms import TaskForm
from .models import Task
from accounts.models import User
from tasks.modules import count_tasks_by_status


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            # 1. ضبط من أنشأ المهمة
            task.created_by = request.user
            
            # 2. تعيين المهمة إلى رئيس القسم (مثلاً)
            department = request.user.department
            manager = User.objects.filter(department=department, role='DEPARTMENT_MANAGER').first()
            task.assigned_to = manager
            
            task.save()
            return redirect('tasks:task-list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_tasks.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.filter(created_by=request.user.id)
    total = count_tasks_by_status(request)
    return render(request, 'tasks/list_tasks.html', {'tasks': tasks, 'count_tasks': total})

@login_required
def update_task(request, task_pk):
    task = get_object_or_404(Task, task_pk=task_pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task-list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/modify_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, task_pk):
    task = Task.objects.get(task_pk=task_pk)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:task-list')
    return render(request, 'tasks/delete_task.html', {'task': task})

@login_required
def is_department_manager(user):
    return user.role == 'DEPARTMENT_MANAGER'

@login_required
def is_general_manager(user):
    return user.role == 'GENERAL_MANAGER'


@login_required
@user_passes_test(is_department_manager)
def department_tasks(request):
    # عرض مهام جميع الموظفين في نفس الإدارة
    tasks = Task.objects.get(id=request.user.id)
    return render(request, 'tasks/department.html', {'tasks': tasks})

@login_required
@user_passes_test(is_general_manager)
def all_tasks(request):
    # عرض جميع المهام للمدير العام
    tasks = Task.objects.all()
    return render(request, 'tasks/all.html', {'tasks': tasks})
