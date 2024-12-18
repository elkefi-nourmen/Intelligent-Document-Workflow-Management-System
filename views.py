from django.http import JsonResponse  # Pour renvoyer les résultats en JSON
from .classifier import DocumentClassifier  # Importer la classe de classification

# Vue pour classifier un document à partir du texte
def classify_document(request):
    """
    Vue pour classifier un document.
    Utilisation : Passer un texte en paramètre GET ou POST.
    Exemple : /classify/?text=VotreTexteIci
    """
    # Récupérer le texte depuis la requête
    text = request.GET.get('text', '')  
    
    # Vérifier si le texte est non vide
    if not text:
        return JsonResponse({'error': 'Aucun texte fourni'}, status=400)
    
    # Initialiser le classificateur
    classifier = DocumentClassifier()
    
    # Faire la prédiction
    category = classifier.predict_category(text)
    
    # Retourner la catégorie en réponse JSON
    return JsonResponse({'category': category})
