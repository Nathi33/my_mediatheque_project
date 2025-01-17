from django import forms


class Creationmembre(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Nom",
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="Prénom",
    )
    email = forms.EmailField(
        required=False,
        label="Email",
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        label="Téléphone",
    )


class Updatemembre(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=False,
        label="Nom",
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label="Prénom",
    )
    email = forms.EmailField(
        required=False,
        label="Email",
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        label="Téléphone",
    )


class LivreForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Titre",
    )
    auteur = forms.CharField(
        max_length=250,
        required=True,
        label="Auteur",
    )
    disponibility = forms.BooleanField(
        initial=True,
        required=True,
        label="Disponible",
    )
    nb_pages = forms.IntegerField(
        required=False,
        label="Nombre de pages",
    )


class DvdForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Titre",
    )
    auteur = forms.CharField(
        max_length=250,
        required=True,
        label="Réalisateur",
    )
    disponibility = forms.BooleanField(
        initial=True,
        required=True,
        label="Disponible",
    )
    genre = forms.CharField(
        required=False,
        label="Genre",
    )


class CdForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Titre",
    )
    auteur = forms.CharField(
        max_length=250,
        required=True,
        label="Artiste",
    )
    disponibility = forms.BooleanField(
        initial=True,
        required=True,
        label="Disponible",
    )
    date_sortie = forms.DateField(
        required=False,
        label="Date de sortie"
    )


class PlateauForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Nom du jeu",
    )
    auteur = forms.CharField(
        max_length=250,
        required=True,
        label="Créateur",
    )
    nombre_joueurs_min = forms.IntegerField(
        required=False,
        label="Nombre de joueurs minimum",
    )
    nombre_joueurs_max = forms.IntegerField(
        required=False,
        label="Nombre de joueurs maximum",
    )
    disponibility = forms.BooleanField(
        required=False,
        initial=False,
        label="Disponible",
    )