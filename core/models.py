from django.db import models
from django.contrib.auth.models import User

# Document Model
class Document(models.Model):
    TYPE_CHOICES = [
        ('Invoice', 'Invoice'),
        ('Contract', 'Contract'),
        ('Report', 'Report'),
    ]
    name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    content = models.TextField()  # Store text-based or link to files
    status = models.CharField(max_length=20, default='Pending')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Workflow Model
class Workflow(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    current_step = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='In Progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)