from django.urls import path
from . import views

app_name = 'reports'


urlpatterns = [
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('department/', views.department_dashboard, name='department-dashboard'),
    path('general/', views.general_dashboard, name='general_dashboard'),
    path('filter/', views.filter_tasks, name='filter_tasks'),
    path('task/<uuid:task_id>/', views.task_details, name='task_details'),
]
