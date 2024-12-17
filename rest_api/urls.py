from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet, DocumentViewSet, WorkflowViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'workflows', WorkflowViewSet, basename='workflow')

urlpatterns = [
    path('',include(router.urls)),
]
