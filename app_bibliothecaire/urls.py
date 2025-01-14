from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_bibliothecaire, name='home_bibliothecaire'),
]