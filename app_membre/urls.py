from django.urls import path
from . import views

app_name = 'app_membre'

urlpatterns = [
    path('', views.member_home, name='home_membre'),
    path('liste_medias_membre/', views.list_medias_member, name='liste_medias_membre'),
]