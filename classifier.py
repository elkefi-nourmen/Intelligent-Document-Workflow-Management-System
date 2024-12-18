import os
import joblib  # Pour charger le modèle sauvegardé
from sklearn.feature_extraction.text import TfidfVectorizer  # Transformer le texte en vecteurs numériques

# Définir le chemin du modèle sauvegardé
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'classifier.pkl')

# Classe pour gérer la classification des documents
class DocumentClassifier:
    def __init__(self):
        # Charger le modèle IA sauvegardé
        self.model = joblib.load(MODEL_PATH)
        # Initialiser le vectorizer pour transformer le texte en vecteur
        self.vectorizer = TfidfVectorizer()

    def predict_category(self, text):
        """
        Prédire la catégorie d'un texte donné.
        :param text: Le texte du document
        :return: La catégorie prédite
        """
        # Transformer le texte en vecteur
        text_vector = self.vectorizer.fit_transform([text])
        # Faire la prédiction
        prediction = self.model.predict(text_vector)
        return prediction[0]
