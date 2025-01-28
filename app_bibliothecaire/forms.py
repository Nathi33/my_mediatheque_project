from django import forms
from .models import Member, Media, Loan
from django.core.exceptions import ValidationError
from datetime import datetime


class Membercreation(forms.Form):
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


class Memberupdate(forms.Form):
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


class BookForm(forms.Form):
    CATEGORIES_CHOICES = [
        ('book', 'Books'),
        ('dvd', 'Dvd'),
        ('cd', 'Cd'),
        ('board', 'Board'),
    ]
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Titre",
    )
    author = forms.CharField(
        max_length=250,
        required=True,
        label="Auteur",
    )
    availability = forms.BooleanField(
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
        required=False,
        initial='book',
    )


class DvdForm(forms.Form):
    CATEGORIES_CHOICES = [
        ('book', 'Books'),
        ('dvd', 'Dvd'),
        ('cd', 'Cd'),
        ('board', 'Board'),
    ]
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Titre",
    )
    author = forms.CharField(
        max_length=250,
        required=True,
        label="Réalisateur",
    )
    availability = forms.BooleanField(
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
        required=False,
        initial='dvd',
    )


class CdForm(forms.Form):
    CATEGORIES_CHOICES = [
        ('book', 'Books'),
        ('dvd', 'Dvd'),
        ('cd', 'Cd'),
        ('board', 'Board'),
    ]
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Titre",
    )
    author = forms.CharField(
        max_length=250,
        required=True,
        label="Artiste",
    )
    availability = forms.BooleanField(
        initial=True,
        required=True,
        label="Disponible",
    )
    release_date = forms.DateField(
        required=False,
        label="Date de sortie"
    )
    categorie = forms.ChoiceField(
        choices=CATEGORIES_CHOICES,
        label="Catégorie",
        required=False,
        initial='cd',
    )


class BoardForm(forms.Form):
    CATEGORIES_CHOICES = [
        ('book', 'Books'),
        ('dvd', 'Dvd'),
        ('cd', 'Cd'),
        ('board', 'Board'),
    ]
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Nom du jeu",
    )
    author = forms.CharField(
        max_length=250,
        required=True,
        label="Créateur",
    )
    number_players_min = forms.IntegerField(
        required=False,
        label="Nombre de joueurs minimum",
    )
    number_players_max = forms.IntegerField(
        required=False,
        label="Nombre de joueurs maximum",
    )
    availability = forms.BooleanField(
        required=False,
        initial=False,
        label="Disponible",
        widget=forms.CheckboxInput(attrs={'disabled': 'disabled'})
    )
    categorie = forms.ChoiceField(
        choices=CATEGORIES_CHOICES,
        label="Catégorie",
        required=False,
        initial='board',
    )


class LoanForm(forms.Form):
    CATEGORIES_CHOICES = [
        ('', ''),
        ('book', 'Books'),
        ('dvd', 'Dvd'),
        ('cd', 'Cd'),
        ('board', 'Board')
    ]
    categorie = forms.ChoiceField(
        choices=CATEGORIES_CHOICES,
        label="Sélectionner une catégorie",
        required=False
    )
    member_id = forms.ModelChoiceField(
        queryset=Member.objects.all(),
        label="Sélectionner un membre",
    )
    media_id = forms.ModelChoiceField(
        queryset=Media.objects.none(),  # Initialement vide
        label="Sélectionner un média",
        required=False
    )
    loan_date = forms.DateTimeField(
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
            self.fields['media_id'].queryset = Media.objects.filter(category=categorie, availability=True)
        else:
            self.fields['media_id'].queryset = Media.objects.filter(availability=True)

    def clean_loan_date(self):
        loan_date = self.cleaned_data['loan_date']
        # Convertir en date uniquement si c'est un datetime
        if isinstance(loan_date, datetime):
            loan_date = loan_date.date()
        # Vérifie si la date est valide, même si elle est passée
        if loan_date > datetime.today().date():
            raise forms.ValidationError("La date d'emprunt ne peut pas être dans le futur.")
        return loan_date


class SelectBorrowerForm(forms.Form):
    borrower = forms.ModelChoiceField(
        queryset=Member.objects.all(),
        label="Sélectionner un emprunteur",
        widget=forms.Select
    )


class ReturnLoanForm(forms.Form):
    loan_id = forms.IntegerField(widget=forms.HiddenInput)
    media_name = forms.CharField(label="Nom du média", required=False, disabled=True)
    loan_date = forms.DateField(label="Date d'emprunt", required=False, disabled=True)
    expected_return_date = forms.DateField(label="Date de retour prévue", required=False, disabled=True)
    effective_return_date = forms.DateTimeField(
        label="Date de retour effective",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )

    def __init__(self, *args, **kwargs):
        loan = kwargs.pop('loan', None)
        super().__init__(*args, **kwargs)
        if loan:
            self.fields['loan_id'].initial = loan.id
            self.fields['media_name'].initial = loan.media.name
            self.fields['loan_date'].initial =loan.loan_date
            self.fields['expected_return_date'].initial = loan.expected_return_date

    def clean_effective_return_date(self):
        # Validation de la date de retour effective
        effective_return_date = self.cleaned_data['effective_return_date']
        loan_id = self.cleaned_data.get('loan_id')
        try:
            loan = Loan.objects.get(id=loan_id)
        except Loan.DoesNotExist:
            raise ValidationError("L'emprunt sélectionné n'existe pas.")

        # Si date_retour_effective est un datetime, la convertir en date
        if isinstance(effective_return_date, datetime):
            effective_return_date = effective_return_date.date()

        # Vérifie que la date de retour effective est postérieure à la date d'emprunt
        if effective_return_date < loan.loan_date.date():
            raise ValidationError("La date de retour effective ne peut pas être antérieure à la date d'emprunt.")

        # Vérifie si l'emprunt a déjà été retourné
        if loan.effective_return_date:
            raise ValidationError("Cet emprunt a déjà été retourné.")

        return effective_return_date

    def save(self):
        # Enregistre un retour d'emprunt
        loan_id = self.cleaned_data['loan_id']
        effective_return_date = self.cleaned_data['effective_return_date']
        loan = Loan.objects.get(id=loan_id)

        # Mise à jour de la date de retour effective
        loan.effective_return_date = effective_return_date
        loan.media.availability = True  # Rend le média disponible après retour
        loan.media.save()
        loan.save()

        return loan
