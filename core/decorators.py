from django.contrib.auth.decorators import user_passes_test

def admin_required(function=None):
    """Limit view to administrators only."""
    actual_decorator = user_passes_test(
        lambda user: user.is_authenticated and user.groups.filter(name='Administrator').exists(),
        login_url='login',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def manager_required(function=None):
    """Limit view to managers only."""
    actual_decorator = user_passes_test(
        lambda user: user.is_authenticated and user.groups.filter(name='Manager').exists(),
        login_url='login',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def employee_required(function=None):
    """Limit view to employees only."""
    actual_decorator = user_passes_test(
        lambda user: user.is_authenticated and user.groups.filter(name='Employee').exists(),
        login_url='login',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
