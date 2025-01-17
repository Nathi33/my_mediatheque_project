from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'), # Page d'accueil générale
    path('bibliothecaire/', include('app_bibliothecaire.urls'), name='bibliothecaire'), #Page d'accueil pour les bibliothécaires
    path('membre/', include('app_membre.urls'), name='membre'), #Page d'accueil pour les membres
]
