from django.shortcuts import render, redirect, get_object_or_404
from app_bibliothecaire.models import Membre, Livre, Dvd, Cd, Plateau, Emprunt, Media
from app_bibliothecaire.forms import (Creationmembre, Updatemembre, LivreForm, DvdForm,
                                      CdForm, PlateauForm, EmpruntForm, SelectEmprunteurForm, RetourEmpruntForm)
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


# Fonctionnalité : Menu principal
def home_bibliothecaire(request):
    return render(request, 'app_biblio/home_bibliothecaire.html')


# Fonctionnalités : Membre
def listemembres(request):
    #La variable membres récupère tous les objets de la table Membre dans la BDD
    membres = Membre.objects.all()
    #La fonction render() est utilisée pr renvoyer une réponse HTTP ac un template HTML ici : 'membres/listmembres.html'
    #La clé 'membres' devient une variable accessible dans le template
    #membres est une valeur associée à cette clé, c'est la liste des objets Membre récupérés
    return render(request, 'membres/listmembres.html', {'membres': membres})


def ajoutmembre(request):
    #Vérification de la méthode HTTP : si POST le formulaire a été soumis sinon l'afficher pour le remplir
    if request.method == 'POST':
        #Création d'une instance du formulaire avec les données envoyées par l'utilisateur via le formulaire
        creationmembre = Creationmembre(request.POST)
        #Vérifie que toutes les contraintes du formulaire sont respectées
        if creationmembre.is_valid():
            #Si le formulaire est valide, une instance vide du modèle Membre est créée
            membre = Membre()
            #Les données du formulaire sont récupérées à l'aide de creationmembre.cleaned_data qui contiennet les
            #données valides
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
            emprunteur = form.cleaned_data['membre_id']
            media = form.cleaned_data['media_id']

            emprunt = Emprunt(emprunteur=emprunteur, media=media)
            emprunt.save()

            messages.success(request, "Emprunt créé avec succès !")
            return HttpResponseRedirect(reverse('app_bibliothecaire:creer_emprunt'))

    return render(request, 'emprunt/creer_emprunt.html', {'form': form})



def retour_emprunt(request):
    if 'emprunteur_id' not in request.GET:
        # Étape 1 : Sélection de l'emprunteur
        if request.method == 'POST':
            form = SelectEmprunteurForm(request.POST)
            if form.is_valid():
                emprunteur = form.cleaned_data['emprunteur']
                return redirect(f"{request.path}?emprunteur_id={emprunteur.id}")
        else:
            form = SelectEmprunteurForm()
        return render(request, 'emprunt/select_emprunteur.html', {'form': form})

    # Étape 2 : Gestion des emprunts pour l'emprunteur sélectionné
    emprunteur_id = request.GET.get('emprunteur_id')
    emprunteur = get_object_or_404(Membre, id=emprunteur_id)
    emprunts = Emprunt.objects.filter(emprunteur=emprunteur, date_retour_effective__isnull=True)

    if request.method == 'POST':
        form = RetourEmpruntForm(request.POST)
        if form.is_valid():
            # Sauvegarde l'emprunt retourné
            emprunt = form.save()

            # Mettre à jour la disponibilité du média après le retour
            media = emprunt.media # On récupère le média lié à l'emprunt
            media.disponibility = True # Le média devient disponible
            media.save() # On enregistre la modification

            # Rediriger après la mise à jour
            return redirect(f"{request.path}?emprunteur_id={emprunteur.id}")
    else:
        forms = [RetourEmpruntForm(emprunt=emprunt) for emprunt in emprunts]

    return render(request, 'emprunt/retour_emprunt.html', {
        'emprunteur': emprunteur,
        'forms': forms
    })


def deletemedia(request, id):
    media = get_object_or_404(Media, pk=id)
    media.delete()
    messages.success(request, "Le media a été supprimé avec succès !")
    return redirect('app_bibliothecaire:listmedia')


