from django.shortcuts import render, redirect, get_object_or_404
from app_bibliothecaire.models import Membre, Livre, Dvd, Cd, Plateau, Emprunt, Media
from app_bibliothecaire.forms import (Creationmembre, Updatemembre, LivreForm, DvdForm,
                                      CdForm, PlateauForm, EmpruntForm, SelectEmprunteurForm, RetourEmpruntForm)
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import timedelta


# Fonctionnalité : Menu principal
def home_bibliothecaire(request):
    return render(request, 'app_biblio/home_bibliothecaire.html')


# Fonctionnalités : Membre
def listemembres(request):
    # La variable membres récupère tous les objets de la table Membre dans la BDD
    membres = Membre.objects.all()
    for membre in membres:
        # Filtre les emprunts en cours pour chaque membre
        membre.emprunts_en_cours = Emprunt.objects.filter(emprunteur=membre, date_retour_effective__isnull=True)
    # La fonction render() est utilisée pr renvoyer une réponse HTTP ac un template HTML ici : 'membres/listmembres.html'
    # La clé 'membres' devient une variable accessible dans le template
    # membres est une valeur associée à cette clé, c'est la liste des objets Membre récupérés
    return render(request, 'membres/listmembres.html', {'membres': membres})


def ajoutmembre(request):
    # Vérification de la méthode HTTP : si POST le formulaire a été soumis sinon l'afficher pour le remplir
    if request.method == 'POST':
        # Création d'une instance du formulaire avec les données envoyées par l'utilisateur via le formulaire
        creationmembre = Creationmembre(request.POST)
        # Vérifie que toutes les contraintes du formulaire sont respectées
        if creationmembre.is_valid():
            # Si le formulaire est valide, une instance vide du modèle Membre est créée
            membre = Membre()
            # Les données du formulaire sont récupérées à l'aide de creationmembre.cleaned_data qui contiennet les
            # données valides
            membre.name = creationmembre.cleaned_data['name']
            membre.first_name = creationmembre.cleaned_data['first_name']
            membre.email = creationmembre.cleaned_data['email']
            membre.phone = creationmembre.cleaned_data['phone']
            #Enregistre le nouvel objet Membre dans la base de données
            membre.save()
            #Notification de confirmation de création
            messages.success(request, "Le membre a été mis ajouté avec succès !")
            return redirect('app_bibliothecaire:listmembres')
        #Si le formulaire n'est pas valide, la page ajoutmembre est réaffichée avec le formulaire rempli 'creationMembre
        #indiquant les erreurs ou champs manquants
        else:
            return render(request, 'membres/ajoutmembre.html', {'creationMembre': creationmembre})
    #Si la méthode HTTP est GET, une instance vide du formulaire est créée et
    # la page ajoutmembre.html est affichée avec le formulaire vide
    else:
        creationmembre = Creationmembre()
        return render(request, 'membres/ajoutmembre.html', {'creationMembre': creationmembre})



def updatemembre(request, id):
    #Récupère l'objet Membre correspondant à l'ID fourni
    #Si aucun membre avec l'ID n'existe alors une page 404 est envoyée
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
    #Si la méthode est GET, une instance du formulaire Updatemembre est créée,
    #les champs du formulaire sont pré-remplis avec les données existantes du membre (initial={...})
    else:
        update_membre = Updatemembre(initial={
            'name' : membre.name,
            'first_name' : membre.first_name,
            'email' : membre.email,
            'phone' : membre.phone,
        })
    return render(request, 'membres/updatemembre.html', {'updatemembre': update_membre})


def deletemembre(request, id):
    membre = get_object_or_404(Membre, pk=id)
    membre.delete()
    messages.success(request, "Le membre a été supprimé avec succès !")
    return redirect('app_bibliothecaire:listmembres')


# Fonctionnalités : Média
def listemedia(request):
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
    # Ici la variable 'context' permet de regrouper les données tq {'livres': livres, 'dvds': dvds, ...)
    return render(request, 'media/listmedia.html', context)


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


