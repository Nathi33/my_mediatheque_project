from django import forms
from .models import Membre, Media, Emprunt
from django.core.exceptions import ValidationError
from datetime import datetime


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
        required=False,  # Permet de ne pas forcer la sélection
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
        widget=forms.CheckboxInput(attrs={'disabled': 'disabled'})
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
        queryset=Media.objects.none(),  # Initialement vide
        label="Sélectionner un média",
        required=False
    )
    date_emprunt = forms.DateTimeField(
        label="Date de l'emprunt",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )

    def __init__(self, *args, **kwargs):
        categorie = kwargs.pop('categorie', None)  # Récupère la catégorie depuis la vue
        super().__init__(*args, **kwargs)

        # Si une catégorie est renseignée, on filtre les médias par cette catégorie
        if categorie:
            self.fields['media_id'].queryset = Media.objects.filter(category=categorie, disponibility=True)
        else:
            self.fields['media_id'].queryset = Media.objects.filter(disponibility=True)

    def clean_date_emprunt(self):
        date_emprunt = self.cleaned_data['date_emprunt']
        # Convertir en date uniquement si c'est un datetime
        if isinstance(date_emprunt, datetime):
            date_emprunt = date_emprunt.date()
        # Vérifie si la date est valide, même si elle est passée
        if date_emprunt > datetime.today().date():
            raise forms.ValidationError("La date d'emprunt ne peut pas être dans le futur.")
        return date_emprunt


class SelectEmprunteurForm(forms.Form):
    emprunteur = forms.ModelChoiceField(
        queryset=Membre.objects.all(),
        label="Sélectionner un emprunteur",
        widget=forms.Select
    )


class RetourEmpruntForm(forms.Form):
    emprunt_id = forms.IntegerField(widget=forms.HiddenInput)
    media_name = forms.CharField(label="Nom du média", required=False, disabled=True)
    date_emprunt = forms.DateField(label="Date d'emprunt", required=False, disabled=True)
    date_retour_prevue = forms.DateField(label="Date de retour prévue", required=False, disabled=True)
    date_retour_effective = forms.DateTimeField(
        label="Date de retour effective",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )

    def __init__(self, *args, **kwargs):
        emprunt = kwargs.pop('emprunt', None)
        super().__init__(*args, **kwargs)
        if emprunt:
            self.fields['emprunt_id'].initial = emprunt.id
            self.fields['media_name'].initial = emprunt.media.name
            self.fields['date_emprunt'].initial = emprunt.date_emprunt
            self.fields['date_retour_prevue'].initial = emprunt.date_retour_prevue

    def clean_date_retour_effective(self):
        # Validation de la date de retour effective
        date_retour_effective = self.cleaned_data['date_retour_effective']
        emprunt_id = self.cleaned_data.get('emprunt_id')
        try:
            emprunt = Emprunt.objects.get(id=emprunt_id)
        except Emprunt.DoesNotExist:
            raise ValidationError("L'emprunt sélectionné n'existe pas.")

        # Si date_retour_effective est un datetime, la convertir en date
        if isinstance(date_retour_effective, datetime):
            date_retour_effective = date_retour_effective.date()

        # Vérifie que la date de retour effective est postérieure à la date d'emprunt
        if date_retour_effective < emprunt.date_emprunt.date():
            raise ValidationError("La date de retour effective ne peut pas être antérieure à la date d'emprunt.")

        # Vérifie si l'emprunt a déjà été retourné
        if emprunt.date_retour_effective:
            raise ValidationError("Cet emprunt a déjà été retourné.")

        return date_retour_effective

    def save(self):
        # Enregistre un retour d'emprunt
        emprunt_id = self.cleaned_data['emprunt_id']
        date_retour_effective = self.cleaned_data['date_retour_effective']
        emprunt = Emprunt.objects.get(id=emprunt_id)

        # Mise à jour de la date de retour effective
        emprunt.date_retour_effective = date_retour_effective
        emprunt.media.disponibility = True  # Rend le média disponible après retour
        emprunt.media.save()
        emprunt.save()

        return emprunt
