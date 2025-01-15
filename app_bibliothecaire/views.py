from django.shortcuts import render, redirect, get_object_or_404
from app_bibliothecaire.models import Membre
from app_bibliothecaire.forms import Creationmembre, Updatemembre
from django.contrib import messages


def home_bibliothecaire(request):
    return render(request, 'app_bibliothecaire/home_bibliothecaire.html')


def listemembres(request):
    membres = Membre.objects.all()
    return render(request, 'membres/listmembres.html', {'membres': membres})


def ajoutmembre(request):
    if request.method == 'POST':
        creationmembre = Creationmembre(request.POST)
        if creationmembre.is_valid():
            membre = Membre()
            membre.name = creationmembre.cleaned_data['name']
            membre.first_name = creationmembre.cleaned_data['first_name']
            membre.email = creationmembre.cleaned_data['email']
            membre.phone = creationmembre.cleaned_data['phone']
            membre.save()
            messages.success(request, "Le membre a été mis ajouté avec succès.")
            return redirect('listmembres')
        else:
            return render(request, 'membres/ajoutmembre.html', {'creationMembre': creationmembre})
    else:
        creationmembre = Creationmembre()
        return render(request, 'membres/ajoutmembre.html', {'creationMembre': creationmembre})



def updatemembre(request, id):
    membre = get_object_or_404(Membre, pk=id)
    if request.method == 'POST':
        update_membre = Updatemembre(request.POST)
        if update_membre.is_valid():
            membre.name = update_membre.cleaned_data['name']
            membre.first_name = update_membre.cleaned_data['first_name']
            membre.email = update_membre.cleaned_data['email']
            membre.phone = update_membre.cleaned_data['phone']
            membre.save()
            messages.success(request, "Le membre a été mis à jour avec succès.")
        return redirect('listmembres')
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
    messages.success(request, "Le membre a été supprimé avec succès")
    return redirect('listmembres')
