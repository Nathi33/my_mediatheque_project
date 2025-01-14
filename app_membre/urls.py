from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_membre, name='home_membre'),
]