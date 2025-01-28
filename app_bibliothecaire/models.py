from django.db import models
from django.utils import timezone
from datetime import timedelta


class Member(models.Model):
    """ Modèle de base d'un Membre.
    Attributs :
        name (str) : Nom du membre.
        first_name (str) : Prénom du membre.
        email (str) : Adresse email du membre (facultatif).
        phone (str) : Numéro de téléphone du membre (facultatif).
        creation_date (datetime) : Date de création du compte du membre.
    """
    name = models.fields.CharField(max_length=150)
    first_name = models.fields.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """ Retourne une représentation textuelle de l'objet.
        Exemple : "Doe John"
        """
        return f"{self.name} {self.first_name}"


class Media(models.Model):
    """ Modèle de base d'un Média.
    Attributs :
        name (str) : Nom du média.
        author (str) : Auteur ou créateur du média.
        category (str) : Catégorie du média (choix parmi 'livre', 'dvd', 'cd', 'plateau').
        availability (bool) : Indique si le média est disponible pour l'emprunt.
        borrower (Member) : Référence vers le membre ayant emprunté ce média.
        loan_date (datetime) : Date de l'emprunt.
    """

    CATEGORY_CHOICES = [
        ('book', 'Book'),
        ('dvd', 'Dvd'),
        ('cd', 'Cd'),
        ('board', 'Board'),
    ]
    name = models.fields.CharField(max_length=150)
    author = models.fields.CharField(max_length=250)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='book')
    availability = models.BooleanField(default=True)
    borrower = models.ForeignKey(Member, null=True, blank=True, on_delete=models.SET_NULL)
    loan_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(Media):
    """ Modèle de base d'un livre.
    Attributs supplémentaires :
        nb_pages (int) : Nombre de pages du livre.
    """
    nb_pages = models.IntegerField(null=True, blank=True)


class Dvd(Media):
    genre = models.fields.CharField(max_length=250, null=True, blank=True)


class Cd(Media):
    release_date = models.DateField(null=True, blank=True)


class Board(Media):
    number_players_min = models.IntegerField(null=True, blank=True)
    number_players_max = models.IntegerField(null=True, blank=True)


def get_default_loan_date():
    # Calcule la date de retour prévue en fonction de la date d'emprunt
    return timezone.now().date() + timedelta(days=7)


class Loan(models.Model):
    """ Modèle de base de l'emprunt d'un média par un membre.
    Attributs :
        borrower (Member) : Référence vers le membre qui emprunte.
        media (Media) : Référence vers le média emprunté.
        loan_date (datetime) : Date de l'emprunt.
        expected_return_date (date) : Date prévue pour le retour.
        effective_return_date (date) : Date réelle du retour.
    """
    borrower = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="loans"
    )
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="loans"
    )
    loan_date = models.DateTimeField(null=True, blank=True)
    expected_return_date = models.DateField(default=get_default_loan_date)
    effective_return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.media.name} emprunté par {self.borrower}"

    def check_borrowing_limit(self):
        """ Vérifie si le membre a atteint la limite de 3 emprunts actifs
        et
        lève une exception ValueError si la limite est atteinte.
        """
        active_loans = Loan.objects.filter(
            borrower=self.borrower,
            effective_return_date__isnull=True
        ).count()
        if active_loans >= 3:
            raise ValueError(f"{self.borrower} a déjà 3 emprunts actifs")

    def check_late_loans(self):
        """ Vérifie si le membre a des emprunts en retard
        et
        lève une exception ValueError si un retard est détecté.
        """
        late_loans = Loan.objects.filter(
            borrower=self.borrower,
            effective_return_date__isnull=True,
            expected_return_date__lt=timezone.now().date()
        )
        if late_loans.exists():
            raise ValueError(
                f"{self.borrower} a des emprunts en retard et ne peut paas emprunter de nouveaux médias.")

    def check_availability_media(self):
        if not self.media.availability:
            raise ValueError(f"{self.media.name} n'est pas disponible à l'emprunt.")

    def mark_media_as_available(self):
        self.media.availability = True
        self.media.save()

    def mark_media_as_unavailable(self):
        self.media.availability = False
        self.media.save()

    def save(self, *args, **kwargs):
        """ Save applique les règles de validation avant l'enregistrement :
                - Vérifie les emprunts en cours.
                - Vérifie la disponibilité du média.
                - Marque le média comme non disponible si l'emprunt est actif.
        """
        if self.effective_return_date:
            self.mark_media_as_available()
        else:
            self.check_availability_media()
            self.check_borrowing_limit()
            self.check_late_loans()
            if not self.loan_date:
                self.loan_date = timezone.now().date()
            if not self.expected_return_date:
                self.expected_return_date = self.loan_date + timedelta(days=7)
            self.mark_media_as_unavailable()
        super().save(*args, **kwargs)
