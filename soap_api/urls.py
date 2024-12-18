from django.urls import path
from .views import soap_application

urlpatterns = [
    path('', soap_application),
]
