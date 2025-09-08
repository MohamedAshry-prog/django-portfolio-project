from django.urls import path
from .views import create_task, task_list, department_tasks, all_tasks, update_task, delete_task

app_name = 'tasks'


urlpatterns = [
    path('', task_list, name='task-list'),
    path('update/tasks/<uuid:task_pk>', update_task, name='update-tasks'),
    path('create', create_task , name='task-create'),
    path('task/create/', all_tasks , name='all-tasks'),
    path('delete/tasks/<uuid:task_pk>', delete_task, name='delete-tasks'),
]