from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from django.contrib.auth.models import User
from core.models import Document
from .serializers import UserSerializer, DocumentSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only admin users can manage users


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.created_by == request.user

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        # Employees can only see their own documents
        if not self.request.user.is_staff:
            return Document.objects.filter(uploaded_by=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the creator of the document
        serializer.save(uploaded_by=self.request.user)