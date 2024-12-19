from django.conf import settings
from django.urls import include, path
from . import views
from django.conf.urls.static import static

urlpatterns = [    
    # User Authentication
    path('signup/', views.signup_view, name='signup'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),

    #admin
    path('user_management/', views.user_management, name='user_management'),
    path('user_management/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('user_management/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('workflow_management/', views.workflow_management, name='workflow_management'),
    path('admin_document_management/', views.admin_document_management, name='admin_document_management'),
    path('admin_document_management/delete/<int:document_id>/', views.delete_document, name='delete_document'),
    
    #manager
    path('team_documents/', views.team_documents, name='team_documents'),
    path('document_analytics/', views.document_analytics, name='document_analytics'),
    path('review_document/<int:doc_id>/', views.review_document, name='review_document'),
    path('pending_approvals/', views.pending_approvals, name='pending_approvals'),

    path('task_management/', views.task_management, name='task_management'),
    path('add_workflow/', views.add_workflow, name='add_workflow'),
    path('edit_workflow/<int:workflow_id>/', views.edit_workflow, name='edit_workflow'),
    path('delete_workflow/<int:workflow_id>/', views.delete_workflow, name='delete_workflow'),
]
