from django.shortcuts import render
from app_bibliothecaire.models import Media


def home_membre(request):
    return render(request, 'app_memb/home_membre.html')


def liste_medias(request):
    medias = Media.objects.all()
    return render(request, 'app_memb/liste_medias.html', {'medias': medias})