from django.urls import path
from . import views

app_name = 'app_bibliothecaire'

urlpatterns = [
    path('', views.home_bibliothecaire, name='home_bibliothecaire'),
    path('listmembres/', views.listemembres, name='listmembres'),
    path('ajoutmembre/', views.ajoutmembre, name='ajoutmembre'),
    path('updatemembre/<int:id>/', views.updatemembre, name='updatemembre'),
    path('deletemembre/<int:id>/', views.deletemembre, name='deletemembre'),
    path('listmedia/', views.listemedia, name='listmedia'),
    path('ajoutmedia/', views.ajoutmedia, name='ajoutmedia'),
    path('ajout_livre/', views.ajout_livre, name='ajout_livre'),
    path('ajout_dvd/', views.ajout_dvd, name='ajout_dvd'),
    path('ajout_cd/', views.ajout_cd, name='ajout_cd'),
    path('ajout_plateau/', views.ajout_plateau, name='ajout_plateau'),
    path('creer_emprunt/', views.creer_emprunt, name='creer_emprunt'),
    path('retour_emprunt/', views.retour_emprunt, name='retour_emprunt'),
    path('deletemedia/<int:id>/', views.deletemedia, name='deletemedia'),
]