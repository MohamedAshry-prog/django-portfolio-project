from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.contrib import messages


def LoginView(request):
    if request.user.is_authenticated:  # Fixed: lowercase user
        return redirect('/accounts/profile/data') 
    else:
        if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")
            print(f"Username: {username}, Password: {password}")
            if username and password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    # Get the next URL from the query parameters or default to tasks
                    next_url = request.GET.get('next', '/accounts/profile/data')
                    return redirect(next_url)
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    response = redirect('/accounts/login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required
def profile_data(request):
    user_data = User.objects.get(id = request.user.id)
    return render(request, 'tasks/profile_data.html', {'user': user_data})


@login_required
def handler404(request, exception):
    context = {
        'request_path': request.path,
        'exception': str(exception),
    }
    return render(request, '404.html', context, status=404)