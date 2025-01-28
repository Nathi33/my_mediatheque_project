from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from app_bibliothecaire.models import Membre, Livre, Dvd, Cd, Plateau, Emprunt, Media
from app_bibliothecaire.forms import (Creationmembre, Updatemembre, LivreForm, DvdForm,
                                      CdForm, PlateauForm, EmpruntForm, SelectEmprunteurForm, RetourEmpruntForm)
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import timedelta
import logging

# Création du logger
logger = logging.getLogger(__name__)


# Fonctionnalité : Menu principal
@login_required
def home_bibliothecaire(request):
    logger.info("Accès à la page d'accueil du bibliothécaire.")
    return render(request, 'app_biblio/home_bibliothecaire.html')


# Fonctionnalités : Membre
def listemembres(request):
    """ Affiche la liste des membres.
        Pour chaque membre, récupère les emprunts en cours et les inclut dans l'objet membre.
        En cas d'erreur, une redirection vers la page d'accueil est effectuée avec un message.

        Paramètres :
            - request (HttpRequest) : L'objet requête HTTP.

        Retour :
            - HttpResponse : Rendu de la page 'membres/listmembres.html' avec le contexte :
                - membres (QuerySet) : Liste des membres et leurs emprunts.
            - HttpResponseRedirect : Redirection vers la page d'accueil en cas d'erreur.
        """
    logger.info("Accès à la liste des membres.")
    try:
        membres = Membre.objects.all()
        for membre in membres:
            membre.emprunts_en_cours = Emprunt.objects.filter(emprunteur=membre, date_retour_effective__isnull=True)
            logger.debug(f"{len(membres)} membres récupérés.")
            return render(request, 'membres/listmembres.html', {'membres': membres})
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des membres : {e}", exc_info=True)
        messages.error(request, "Erreur lors du chargement des membres.")
        return redirect('app_bibliothecaire:home_bibliothecaire')


def ajoutmembre(request):
    """ Gère l'ajout d'un nouveau membre.

        Affiche un formulaire d'ajout de membre. Si la requête est une soumission de formulaire (POST),
        elle valide les données et enregistre un nouveau membre dans la base de données. En cas d'erreur, un message
        d'erreur est affiché. Si la méthode est GET, un formulaire vide est affiché pour que l'utilisateur puisse saisir
        les informations du membre.

        Args:
            request (HttpRequest): L'objet requête HTTP.

        Returns:
            HttpResponse: La réponse contenant le rendu du formulaire d'ajout de membre ou une redirection vers la liste des membres
                          en cas de succès ou d'erreur.
        """
    logger.info("Soumission du formulaire d'ajout de membre.")
    if request.method == 'POST':
        creationmembre = Creationmembre(request.POST)
        if creationmembre.is_valid():
            try:
                membre = Membre()
                membre.name = creationmembre.cleaned_data['name']
                membre.first_name = creationmembre.cleaned_data['first_name']
                membre.email = creationmembre.cleaned_data['email']
                membre.phone = creationmembre.cleaned_data['phone']
                membre.save()
                logger.info(f"Membre ajouté avec succès : {membre.name} {membre.first_name}")
                messages.success(request, "Le membre a été mis ajouté avec succès !")
                return redirect('app_bibliothecaire:listmembres')
            except Exception as e:
                logger.error(f"Erreur lors de l'ajout du membre : {e}", exc_info=True)
                messages.error(request, "Erreur lors de l'ajout du membre.")
        else:
            logger.warning("Formulaire d'ajout de membre invalide.")
            return render(request, 'membres/ajoutmembre.html', {'creationMembre': creationmembre})
    else:
        logger.info("Affichage de la page d'ajout de membre.")
        creationmembre = Creationmembre()
        return render(request, 'membres/ajoutmembre.html', {'creationMembre': creationmembre})


def updatemembre(request, id):
    """ Permet de mettre à jour les informations d'un membre.

    Paramètres :
        - request (HttpRequest) : La requête HTTP.
        - id (int) : L'ID du membre à mettre à jour.

    Retour :
        - HttpResponse : La page du formulaire de mise à jour ou une redirection après mise à jour réussie.
    """
    membre = get_object_or_404(Membre, pk=id)
    if request.method == 'POST':
        update_membre = Updatemembre(request.POST)
        if update_membre.is_valid():
            membre.name = update_membre.cleaned_data['name']
            membre.first_name = update_membre.cleaned_data['first_name']
            membre.email = update_membre.cleaned_data['email']
            membre.phone = update_membre.cleaned_data['phone']
            membre.save()
            messages.success(request, "Le membre a été mis à jour avec succès !")
        return redirect('app_bibliothecaire:listmembres')
    else:
        update_membre = Updatemembre(initial={
            'name': membre.name,
            'first_name': membre.first_name,
            'email': membre.email,
            'phone': membre.phone,
        })
    return render(request, 'membres/updatemembre.html', {'updatemembre': update_membre})


def deletemembre(request, id):
    """ Permet de supprimer un membre de la bibliothèque.

    Paramètres :
        - request (HttpRequest) : La requête HTTP.
        - id (int) : L'ID du membre à supprimer.

    Retour :
        - HttpResponseRedirect : Redirection vers la liste des membres après suppression.
    """
    logger.info(f"Tentative de suppression du membre avec ID : {id}")
    try:
        membre = get_object_or_404(Membre, pk=id)
        membre.delete()
        logger.info(f"Membre supprimé avec succès : {membre.name} {membre.first_name}")
        messages.success(request, "Le membre a été supprimé avec succès !")
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du membre : {e}", exc_info=True)
        messages.error(request, "Erreur lors de la suppression du membre.")
    return redirect('app_bibliothecaire:listmembres')


# Fonctionnalités : Média
def listemedia(request):
    logger.info("Accès à la liste des médias.")
    try:
        livres = Livre.objects.all()
        dvds = Dvd.objects.all()
        cds = Cd.objects.all()
        plateaux = Plateau.objects.all()

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
        logger.debug(f"Médias récupérés : {len(livres)} livres, {len(dvds)} DVD, {len(cds)} CD, {len(plateaux)} plateaux.")
        return render(request, 'media/listmedia.html', context)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des médias : {e}", exc_info=True)
        messages.error(request, "Erreur lors du chargement des médias.")
        return redirect('app_bibliothecaire:home_bibliothecaire')


def ajoutmedia(request):
    return render(request, 'media/ajoutmedia.html')


def ajout_livre(request):
    if request.method == 'POST':
        livreform = LivreForm(request.POST)
        if livreform.is_valid():
            livre = Livre()
            livre.name = livreform.cleaned_data['name']
            livre.auteur = livreform.cleaned_data['auteur']
            livre.disponibility = livreform.cleaned_data['disponibility']
            livre.nb_pages = livreform.cleaned_data['nb_pages']
            livre.category = livreform.cleaned_data['categorie']
            livre.save()
            messages.success(request, "Le livre a été ajouté à la liste des médias avec succès !")
            return redirect('app_bibliothecaire:ajoutmedia')
        else:
            return render(request, 'media/ajout_livre.html', {'livreForm': livreform})
    else:
        livreform = LivreForm()
        return render(request, 'media/ajout_livre.html', {'livreForm': livreform})


def ajout_dvd(request):
    if request.method == 'POST':
        dvdform = DvdForm(request.POST)
        if dvdform.is_valid():
            dvd = Dvd()
            dvd.name = dvdform.cleaned_data['name']
            dvd.auteur = dvdform.cleaned_data['auteur']
            dvd.disponibility = dvdform.cleaned_data['disponibility']
            dvd.genre = dvdform.cleaned_data['genre']
            dvd.category = dvdform.cleaned_data['categorie']
            dvd.save()
            messages.success(request, "Le DVD a été ajouté à la liste des médias avec succès !")
            return redirect('app_bibliothecaire:ajoutmedia')
        else:
            return render(request, 'media/ajout_dvd.html', {'dvdForm': dvdform})
    else:
        dvdform = DvdForm()
        return render(request, 'media/ajout_dvd.html', {'dvdForm': dvdform})


def ajout_cd(request):
    if request.method == 'POST':
        cdform = CdForm(request.POST)
        if cdform.is_valid():
            cd = Cd()
            cd.name = cdform.cleaned_data['name']
            cd.auteur = cdform.cleaned_data['auteur']
            cd.disponibility = cdform.cleaned_data['disponibility']
            cd.date_sortie = cdform.cleaned_data['date_sortie']
            cd.category = cdform.cleaned_data['categorie']
            cd.save()
            messages.success(request, "Le CD a été ajouté à la liste des médias avec succès !")
            return redirect('app_bibliothecaire:ajoutmedia')
        else:
            return render(request, 'media/ajout_cd.html', {'cdForm': cdform})
    else:
        cdform = CdForm()
        return render(request, 'media/ajout_cd.html', {'cdForm': cdform})


def ajout_plateau(request):
    if request.method == 'POST':
        plateauform = PlateauForm(request.POST)
        if plateauform.is_valid():
            plateau = Plateau()
            plateau.name = plateauform.cleaned_data['name']
            plateau.auteur = plateauform.cleaned_data['auteur']
            plateau.nombre_joueurs_min = plateauform.cleaned_data['nombre_joueurs_min']
            plateau.nombre_joueurs_max = plateauform.cleaned_data['nombre_joueurs_max']
            plateau.disponibility = plateauform.cleaned_data['disponibility']
            plateau.category = plateauform.cleaned_data['categorie']
            plateau.save()
            messages.success(request, "Le Plateau de jeux a été ajouté à la liste des médias avec succès !")
            return redirect('app_bibliothecaire:ajoutmedia')
        else:
            return render(request, 'media/ajout_plateau.html', {'plateauForm': plateauform})
    else:
        plateauform = PlateauForm()
        return render(request, 'media/ajout_plateau.html', {'plateauForm': plateauform})


def creer_emprunt(request):
    categorie = request.GET.get('categorie')
    form = EmpruntForm(request.GET or None, categorie=categorie)

    if request.method == 'POST':
        form = EmpruntForm(request.POST, categorie=categorie)
        if form.is_valid():
            try:
                emprunteur = form.cleaned_data['membre_id']
                media = form.cleaned_data['media_id']
                date_emprunt = form.cleaned_data['date_emprunt']

                # Calculer la date de retour en fonction de la date d'emprunt
                date_retour_prevue = date_emprunt + timedelta(days=7)

                emprunt = Emprunt(emprunteur=emprunteur,
                                  media=media,
                                  date_emprunt=date_emprunt,
                                  date_retour_prevue=date_retour_prevue)
                emprunt.save()

                messages.success(request, "Emprunt créé avec succès !")
                return HttpResponseRedirect(reverse('app_bibliothecaire:creer_emprunt'))
            except ValueError as e:
                messages.error(request, str(e))

    return render(request, 'emprunt/creer_emprunt.html', {'form': form})


def retour_emprunt(request):
    # Étape 1 : Sélection de l'emprunteur
    if 'emprunteur_id' not in request.GET:
        if request.method == 'POST':
            form = SelectEmprunteurForm(request.POST)
            if form.is_valid():
                emprunteur = form.cleaned_data['emprunteur']
                return redirect(f"{request.path}?emprunteur_id={emprunteur.id}")
        else:
            form = SelectEmprunteurForm()
        return render(request, 'emprunt/select_emprunteur.html', {'form': form})

    # Étape 2 : Affichage des emprunts pour le membre sélectionné
    emprunteur_id = request.GET.get('emprunteur_id')
    emprunteur = get_object_or_404(Membre, id=emprunteur_id)
    emprunts = Emprunt.objects.filter(emprunteur=emprunteur, date_retour_effective__isnull=True)

    # Étape 3 : Gestion du retour d'un emprunt spécifique
    if 'emprunt_id' in request.GET:
        emprunt_id = request.GET.get('emprunt_id')
        emprunt = get_object_or_404(Emprunt, id=emprunt_id)

        if request.method == 'POST':
            form = RetourEmpruntForm(request.POST)
            if form.is_valid():
                # Mise à jour des données de l'emprunt
                emprunt.date_retour_effective = form.cleaned_data['date_retour_effective']
                # Sauvegarde les données de retour
                emprunt.save()

                # Mise à jour de la disponibilité du média
                emprunt.media.disponibility = True
                emprunt.media.save()

                # Message de succès et redirection vers la liste des emprunts
                messages.success(request, f"Le retour de '{emprunt.media.name}' a été effectuée avec succès !")
                return redirect(reverse('app_bibliothecaire:retour_emprunt') + f"?emprunteur_id={emprunteur.id}")

        else:
            form = RetourEmpruntForm(initial={
                'emprunt_id': emprunt.id,
                'media_name': emprunt.media.name,
                'date_emprunt': emprunt.date_emprunt,
                'date_retour_prevue': emprunt.date_retour_prevue,
            })

        return render(request, 'emprunt/retour_emprunt_detail.html', {
            'emprunt': emprunt,
            'form': form
        })

    # Affichage de la liste des emprunts pour le membre sélectionné
    return render(request, 'emprunt/retour_emprunt.html', {
        'emprunteur': emprunteur,
        'emprunts': emprunts
    })


def deletemedia(request, id):
    media = get_object_or_404(Media, pk=id)
    media.delete()
    messages.success(request, "Le media a été supprimé avec succès !")
    return redirect('app_bibliothecaire:listmedia')
