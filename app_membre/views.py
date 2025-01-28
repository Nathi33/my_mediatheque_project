from django.shortcuts import render
from app_bibliothecaire.models import Livre, Dvd, Cd, Plateau


def home_membre(request):
    return render(request, 'app_memb/home_membre.html')


def liste_medias_membre(request):
    # Recharge les médias depuis la BDD pour afficher l'état actuel
    livres = Livre.objects.all()
    dvds = Dvd.objects.all()
    cds = Cd.objects.all()
    plateaux = Plateau.objects.all()

    # Permet la prise en compte d'un emprunt en cours
    for livre in livres:
        livre.emprunt_en_cours = livre.emprunts.filter(date_retour_effective__isnull=True).first()
    for dvd in dvds:
        dvd.emprunt_en_cours = dvd.emprunts.filter(date_retour_effective__isnull=True).first()
    for cd in cds:
        cd.emprunt_en_cours = cd.emprunts.filter(date_retour_effective__isnull=True).first()

    context = {
        'livres': livres,
        'dvds': dvds,
        'cds': cds,
        'plateaux': plateaux,
    }
    return render(request, 'app_memb/liste_medias_membre.html', context)
