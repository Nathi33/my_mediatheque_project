from django.shortcuts import render


def home_bibliothecaire(request):
    return render(request, 'app_bibliothecaire/home_bibliothecaire.html')
