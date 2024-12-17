from django.urls import include, path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    #path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    #path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
]
