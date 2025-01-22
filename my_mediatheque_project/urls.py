from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), # Page d'accueil générale
    path('bibliothecaire/', include('app_bibliothecaire.urls'), name='bibliothecaire'), #Page d'accueil pour les bibliothécaires
    path('membre/', include('app_membre.urls'), name='membre'), #Page d'accueil pour les membres
    path('login/', auth_views.LoginView.as_view(template_name='app_biblio/login.html'), name='login'), # Page de connexion
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # Page de déconnexion de l'utilisateur
]
