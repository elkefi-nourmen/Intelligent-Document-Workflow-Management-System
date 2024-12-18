from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Document  
from ai_service.classifier import DocumentClassifier

@receiver(post_save, sender=Document)
def classify_uploaded_document(sender, instance, created, **kwargs):
    """
    Signal pour classifier automatiquement un document après son upload.
    """
    if created:  # Exécuter uniquement pour les nouveaux documents
        classifier = DocumentClassifier()
        # Lire le contenu du fichier (supposé texte ici)
        with instance.file.open() as f:
            text = f.read().decode('utf-8')  # Décoder le fichier en texte
        
        # Prédire la catégorie
        category = classifier.predict_category(text)
        instance.category = category
        instance.save()
