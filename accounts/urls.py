from django.urls import path
from .views import profile_data, LoginView, logout_view, handler404

app_name = 'accounts'

from .views import LoginView, logout_view
urlpatterns = [
    path('login/', LoginView, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/data', profile_data , name='profile'),
    path('handler404/', handler404, name='handler404'),  # This should be a view that handles 404 errors
]