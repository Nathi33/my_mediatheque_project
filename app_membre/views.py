from django.shortcuts import render


def home_membre(request):
    return render(request, 'app_membre/home_membre.html')