from django.urls import path
from . import views 

# Définir les routes
urlpatterns = [
    # Route pour classifier un document
    path('classify/', views.classify_document, name='classify_document'),
]
