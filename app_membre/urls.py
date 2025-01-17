from django.urls import path
from . import views

app_name = 'app_membre'

urlpatterns = [
    path('', views.home_membre, name='home_membre'),
]