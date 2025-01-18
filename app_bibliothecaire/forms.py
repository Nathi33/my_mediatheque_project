from django import forms
from .models import Membre, Media


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
    CATEGORIES_CHOICES = [
        ('livre', 'Livres'),
        ('dvd', 'Dvd'),
        ('cd', 'Cd'),
        ('plateau', 'Plateau'),
    ]
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
    categorie = forms.ChoiceField(
        choices=CATEGORIES_CHOICES,
        label="Catégorie",
        required=False, # Permet de ne pas forcer la sélection
        initial='livre',
    )


class DvdForm(forms.Form):
    CATEGORIES_CHOICES = [
        ('livre', 'Livres'),
        ('dvd', 'Dvd'),
        ('cd', 'Cd'),
        ('plateau', 'Plateau'),
    ]
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
    categorie = forms.ChoiceField(
        choices=CATEGORIES_CHOICES,
        label="Catégorie",
        required=False,  # Permet de ne pas forcer la sélection
        initial='dvd',
    )


class CdForm(forms.Form):
    CATEGORIES_CHOICES = [
        ('livre', 'Livres'),
        ('dvd', 'Dvd'),
        ('cd', 'Cd'),
        ('plateau', 'Plateau'),
    ]
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
    categorie = forms.ChoiceField(
        choices=CATEGORIES_CHOICES,
        label="Catégorie",
        required=False,  # Permet de ne pas forcer la sélection
        initial='cd',
    )


class PlateauForm(forms.Form):
    CATEGORIES_CHOICES = [
        ('livre', 'Livres'),
        ('dvd', 'Dvd'),
        ('cd', 'Cd'),
        ('plateau', 'Plateau'),
    ]
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
    categorie = forms.ChoiceField(
        choices=CATEGORIES_CHOICES,
        label="Catégorie",
        required=False,  # Permet de ne pas forcer la sélection
        initial='plateau',
    )

class EmpruntForm(forms.Form):
    CATEGORIES_CHOICES = [
        ('', ''),
        ('livre', 'Livres'),
        ('dvd', 'Dvd'),
        ('cd', 'Cd'),
        ('plateau', 'Plateau')
    ]
    categorie = forms.ChoiceField(
        choices=CATEGORIES_CHOICES,
        label="Sélectionner une catégorie",
        required=False  # Permet de ne pas forcer la sélection
    )
    membre_id = forms.ModelChoiceField(
        queryset=Membre.objects.all(),
        label="Sélectionner un membre",
    )
    media_id = forms.ModelChoiceField(
        queryset=Media.objects.none(), #Initialement vide
        label="Sélectionner un média",
        required=False
    )

    def __init__(self, *args, **kwargs):
        categorie = kwargs.pop('categorie', None)  # Récupère la catégorie depuis la vue
        super().__init__(*args, **kwargs)

        # Si une catégorie est renseignée, on filtre les médias par cette catégorie
        if categorie:
            self.fields['media_id'].queryset = Media.objects.filter(category=categorie, disponibility=True)
        else:
            self.fields['media_id'].queryset = Media.objects.filter(disponibility=True)

