from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.exceptions import ValidationError
from core.decorators import admin_required, manager_required, employee_required


def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one number.")
    if not any(char.isalpha() for char in password):
        raise ValidationError("Password must contain at least one letter.")


# Signup View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            validate_password(password1)
        except ValidationError as e:
            messages.error(request, e.message)
            return render(request, 'user_authentication/signup.html')

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, 'user_authentication/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'user_authentication/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'user_authentication/signup.html')

        # Create the new user and assign to 'Employee' group
        user = User.objects.create_user(username=username, email=email, password=password1)
        employee_group = Group.objects.get(name='Employee')  # Ensure group exists
        user.groups.add(employee_group)
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')  # Redirect to the login page

    return render(request, 'user_authentication/signup.html')


# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Redirect to role-specific dashboards
            if user.groups.filter(name='Administrator').exists():
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Manager').exists():
                return redirect('manager_dashboard')
            elif user.groups.filter(name='Employee').exists():
                return redirect('employee_dashboard')
            else:
                return redirect('login')
        else:
            return render(request, 'user_authentication/login.html', {'error': 'Invalid username or password'})
    return render(request, 'user_authentication/login.html')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Admin Dashboard View
@login_required
@admin_required
def admin_dashboard(request):
    return render(request, 'user_authentication/admin_dashboard.html')


# Manager Dashboard View
@login_required
@manager_required
def manager_dashboard(request):
    return render(request, 'user_authentication/manager_dashboard.html')


# Employee Dashboard View
@login_required
@employee_required
def employee_dashboard(request):
    return render(request, 'user_authentication/employee_dashboard.html')
