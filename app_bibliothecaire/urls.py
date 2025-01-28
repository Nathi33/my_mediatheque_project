from django.urls import path
from . import views

app_name = 'app_bibliothecaire'

urlpatterns = [
    path('', views.home_librarian, name='home_bibliothecaire'),
    path('listmembres/', views.listmembers, name='listmembres'),
    path('ajoutmembre/', views.addmember, name='ajoutmembre'),
    path('updatemembre/<int:id>/', views.memberupdate, name='updatemembre'),
    path('deletemembre/<int:id>/', views.memberdelete, name='deletemembre'),
    path('listmedia/', views.listmedia, name='listmedia'),
    path('ajoutmedia/', views.addmedia, name='ajoutmedia'),
    path('ajout_livre/', views.add_book, name='ajout_livre'),
    path('ajout_dvd/', views.add_dvd, name='ajout_dvd'),
    path('ajout_cd/', views.add_cd, name='ajout_cd'),
    path('ajout_plateau/', views.add_board, name='ajout_plateau'),
    path('creer_emprunt/', views.create_loan, name='creer_emprunt'),
    path('retour_emprunt/', views.return_loan, name='retour_emprunt'),
    path('deletemedia/<int:id>/', views.mediadelete, name='deletemedia'),
]
