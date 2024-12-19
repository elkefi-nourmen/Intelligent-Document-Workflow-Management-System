import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.exceptions import ValidationError
from core.decorators import admin_required, manager_required, employee_required
from core.models import Document, Workflow

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
            return render(request, 'core/signup.html')

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, 'core/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'core/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'core/signup.html')

        # Create the new user and assign to 'Employee' group
        user = User.objects.create_user(username=username, email=email, password=password1)
        employee_group = Group.objects.get(name='Employee')  # Ensure group exists
        user.groups.add(employee_group)
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')  # Redirect to the login page

    return render(request, 'core/signup.html')


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
                messages.error(request, "User role not assigned.")
                return redirect('login')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})
    return render(request, 'core/login.html')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Admin Dashboard View
@login_required
@admin_required
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')


# Manager Dashboard View
@login_required
@manager_required
def manager_dashboard(request):
    pending_documents = Document.objects.filter(status="pending")
    return render(request, 'core/manager_dashboard.html', {'pending_documents': pending_documents})

# Team Documents View
@login_required
@manager_required
def team_documents(request):
    documents = Document.objects.all()
    return render(request, 'core/team_documents.html', {'documents': documents})


# Task Management View
@login_required
@manager_required
def task_management(request):
    workflows = Workflow.objects.select_related('document', 'assigned_to').all()
    return render(request, 'core/task_management.html', {'workflows': workflows})


# Document Analytics View
@login_required
@manager_required
def document_analytics(request):
    """
    View to show document statistics in a pie chart.
    """
    pending_documents = Document.objects.filter(status="pending").count()
    approved_documents = Document.objects.filter(status="approved").count()
    rejected_documents = Document.objects.filter(status="rejected").count()

    data = {
        'pending': pending_documents,
        'approved': approved_documents,
        'rejected': rejected_documents,
    }

    return render(request, 'core/document_analytics.html', {
        'data_json': json.dumps(data)  # Serialize to JSON
    })


# Review Document View
@login_required
@manager_required
def review_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            document.status = 'approved'
        elif action == 'reject':
            document.status = 'rejected'
        document.save()
        messages.success(request, f"Document '{document.title}' has been {document.status}.")
        return redirect('manager_dashboard')

    return render(request, 'core/review_document.html', {'document': document})


# add workflow view
@login_required
@manager_required
def add_workflow(request):
    if request.method == 'POST':
        document_id = request.POST.get('document_id')
        assigned_to_id = request.POST.get('assigned_to_id')
        status = request.POST.get('status')

        document = get_object_or_404(Document, id=document_id)
        assigned_to = get_object_or_404(User, id=assigned_to_id)

        Workflow.objects.create(
            document=document,
            assigned_to=assigned_to,
            status=status
        )
        messages.success(request, "Workflow added successfully!")
        return redirect('task_management')

    documents = Document.objects.all()
    users = User.objects.filter(groups__name="Employee")
    return render(request, 'core/add_workflow.html', {'documents': documents, 'users': users})

# edit workflow view
@login_required
@manager_required
def edit_workflow(request, workflow_id):
    workflow = get_object_or_404(Workflow, id=workflow_id)

    if request.method == 'POST':
        workflow.status = request.POST.get('status')
        workflow.save()
        messages.success(request, "Workflow updated successfully!")
        return redirect('task_management')

    return render(request, 'core/edit_workflow.html', {'workflow': workflow})


# delete workflow view
@login_required
@manager_required
def delete_workflow(request, workflow_id):
    workflow = get_object_or_404(Workflow, id=workflow_id)
    workflow.delete()
    messages.success(request, "Workflow deleted successfully!")
    return redirect('task_management')


# pending approvals view
@login_required
@manager_required
def pending_approvals(request):
    """
    View to display all documents with a 'pending' status that require manager approval.
    """
    pending_documents = Document.objects.filter(status="pending").select_related('uploaded_by')
    return render(request, 'core/pending_approvals.html', {'pending_documents': pending_documents})



# Employee Dashboard View
@login_required
@employee_required
def employee_dashboard(request):
    if request.method == 'POST':
        # Handle document upload
        title = request.POST.get('title')
        document_type = request.POST.get('document_type')
        file = request.FILES.get('file')

        if not title or not document_type or not file:
            messages.error(request, "All fields are required!")
        else:
            document = Document.objects.create(
                title=title,
                document_type=document_type,
                file=file,
                uploaded_by=request.user
            )
            messages.success(request, "Document uploaded successfully!")

        return redirect('employee_dashboard')

    # Handle GET request: Display employee dashboard and uploaded documents
    documents = Document.objects.filter(uploaded_by=request.user)
    return render(request, 'core/employee_dashboard.html', {'documents': documents})


# user management View
@login_required
@admin_required
def user_management(request):
    users = User.objects.all()
    return render(request, 'core/user_management.html', {'users': users})


# edit user View
@login_required
@admin_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, f"User {user.username}'s details updated successfully!")
        return redirect('user_management')

    return render(request, 'core/edit_user.html', {'user': user})


# delete user View
@login_required
@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f"User {user.username} deleted successfully!")
        return redirect('user_management')

    return render(request, 'core/confirm_delete_user.html', {'user': user})


# workflow management View
@login_required
@admin_required
def workflow_management(request):
    workflows = Workflow.objects.select_related('document', 'assigned_to').all()
    return render(request, 'core/workflow_management.html', {'workflows': workflows})


# Admin Document Management View
@login_required
@admin_required
def admin_document_management(request):
    documents = Document.objects.all()

    if request.method == 'POST':
        # Handle Document Upload
        title = request.POST.get('title')
        document_type = request.POST.get('document_type')
        file = request.FILES.get('file')

        if not title or not document_type or not file:
            messages.error(request, "All fields are required!")
        else:
            Document.objects.create(
                title=title,
                document_type=document_type,
                file=file,
                uploaded_by=request.user
            )
            messages.success(request, "Document uploaded successfully!")

        return redirect('admin_document_management')

    return render(request, 'core/admin_document_management.html', {'documents': documents})


# Admin Document Delete View
@login_required
@admin_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()
    messages.success(request, f"Document '{document.title}' deleted successfully!")
    return redirect('admin_document_management')