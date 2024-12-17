from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Document

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser']

class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.username')
    class Meta:
        model = Document
        fields = ['id', 'title', 'document_type', 'file', 'status', 'uploaded_by', 'uploaded_at', 'updated_at']