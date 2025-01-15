from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_bibliothecaire, name='home_bibliothecaire'),
    path('listmembres/', views.listemembres, name='listmembres'),
    path('ajoutmembre/', views.ajoutmembre, name='ajoutmembre'),
    path('updatemembre/<int:id>/', views.updatemembre, name='updatemembre'),
    path('deletemembre/<int:id>/', views.deletemembre, name='deletemembre'),

]