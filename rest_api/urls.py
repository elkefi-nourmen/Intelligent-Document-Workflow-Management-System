from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet, DocumentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('',include(router.urls)),
]
