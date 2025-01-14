from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home), # Page d'accueil générale
    path('bibliothecaire/', include('app_bibliothecaire.urls')), #Page d'accueil pour les bibliothécaires
    path('membre/', include('app_membre.urls')), #Page d'accueil pour les membres
]
