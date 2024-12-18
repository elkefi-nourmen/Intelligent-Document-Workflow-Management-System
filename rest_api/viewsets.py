from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from django.contrib.auth.models import User
from core.models import Document, Workflow
from .serializers import UserSerializer, DocumentSerializer, WorkflowSerializer
from .cloud_service import upload_to_nextcloud

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
        instance = serializer.save(uploaded_by=self.request.user)

        username = 'chroud.wejdene@gmail.com'
        password = 'Wej2003...'
        directory = '/Documents/'

        file_path = instance.file.path
        file_name = instance.file.name.split('/')[-1]

        result = upload_to_nextcloud(file_path, file_name, username, password, directory)

        if not result['success']:
            instance.status = 'failed'
            instance.save()
            return

class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]