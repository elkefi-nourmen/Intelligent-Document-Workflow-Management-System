from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

def create_groups():
    # Create groups
    admin_group, _ = Group.objects.get_or_create(name='Administrator')
    manager_group, _ = Group.objects.get_or_create(name='Manager')
    employee_group, _ = Group.objects.get_or_create(name='Employee')

    # Assign permissions to the Administrator group
    content_type_user = ContentType.objects.get_for_model(User)
    admin_permissions = Permission.objects.filter(content_type=content_type_user)  # Full access
    admin_group.permissions.set(admin_permissions)

    # Assign permissions to the Manager group
    manager_permissions = Permission.objects.filter(
        codename__in=['view_user', 'view_document', 'change_document','view_workflow', 'add_workflow', 'change_workflow', 'delete_workflow']
    )
    manager_group.permissions.set(manager_permissions)

    # Assign permissions to the Employee group
    employee_permissions = Permission.objects.filter(
        codename__in=['view_document', 'add_document', 'change_document', 'delete_document']
    )
    employee_group.permissions.set(employee_permissions)

    print("Groups and permissions created successfully.")
