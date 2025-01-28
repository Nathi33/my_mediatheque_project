from django.db import models
from django.utils import timezone
from datetime import timedelta


class Membre(models.Model):
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
        auteur (str) : Auteur ou créateur du média.
        category (str) : Catégorie du média (choix parmi 'livre', 'dvd', 'cd', 'plateau').
        disponibility (bool) : Indique si le média est disponible pour l'emprunt.
        emprunteur (Membre) : Référence vers le membre ayant emprunté ce média.
        date_emprunt (datetime) : Date de l'emprunt.
    """

    CATEGORY_CHOICES = [
        ('livre', 'Livre'),
        ('dvd', 'Dvd'),
        ('cd', 'Cd'),
        ('plateau', 'Plateau'),
    ]
    name = models.fields.CharField(max_length=150)
    auteur = models.fields.CharField(max_length=250)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='livre')
    disponibility = models.BooleanField(default=True)
    emprunteur = models.ForeignKey(Membre, null=True, blank=True, on_delete=models.SET_NULL)
    date_emprunt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Livre(Media):
    """ Modèle de base d'un livre.
    Attributs supplémentaires :
        nb_pages (int) : Nombre de pages du livre.
    """
    nb_pages = models.IntegerField(null=True, blank=True)


class Dvd(Media):
    genre = models.fields.CharField(max_length=250, null=True, blank=True)


class Cd(Media):
    date_sortie = models.DateField(null=True, blank=True)


class Plateau(Media):
    nombre_joueurs_min = models.IntegerField(null=True, blank=True)
    nombre_joueurs_max = models.IntegerField(null=True, blank=True)


def get_default_date_emprunt():
    # Calcule la date de retour prévue en fonction de la date d'emprunt
    return timezone.now().date() + timedelta(days=7)


class Emprunt(models.Model):
    """ Modèle de base de l'emprunt d'un média par un membre.
    Attributs :
        emprunteur (Membre) : Référence vers le membre qui emprunte.
        media (Media) : Référence vers le média emprunté.
        date_emprunt (datetime) : Date de l'emprunt.
        date_retour_prevue (date) : Date prévue pour le retour.
        date_retour_effective (date) : Date réelle du retour.
    """
    emprunteur = models.ForeignKey(
        Membre,
        on_delete=models.CASCADE,
        related_name="emprunts"
    )
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="emprunts"
    )
    date_emprunt = models.DateTimeField(null=True, blank=True)
    date_retour_prevue = models.DateField(default=get_default_date_emprunt)
    date_retour_effective = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.media.name} emprunté par {self.emprunteur}"

    def verifier_nblimite_emprunts(self):
        """ Vérifie si le membre a atteint la limite de 3 emprunts actifs
        et
        lève une exception ValueError si la limite est atteinte.
        """
        emprunts_actifs = Emprunt.objects.filter(
            emprunteur=self.emprunteur,
            date_retour_effective__isnull=True
        ).count()
        if emprunts_actifs >= 3:
            raise ValueError(f"{self.emprunteur} a déjà 3 emprunts actifs")

    def verifier_emprunts_en_retard(self):
        """ Vérifie si le membre a des emprunts en retard
        et
        lève une exception ValueError si un retard est détecté.
        """
        emprunts_en_retard = Emprunt.objects.filter(
            emprunteur=self.emprunteur,
            date_retour_effective__isnull=True,
            date_retour_prevue__lt=timezone.now().date()
        )
        if emprunts_en_retard.exists():
            raise ValueError(
                f"{self.emprunteur} a des emprunts en retard et ne peut paas emprunter de nouveaux médias.")

    def verifier_disponibilite_media(self):
        if not self.media.disponibility:
            raise ValueError(f"{self.media.name} n'est pas disponible à l'emprunt.")

    def marquer_media_comme_disponible(self):
        self.media.disponibility = True
        self.media.save()

    def marquer_media_comme_non_disponible(self):
        self.media.disponibility = False
        self.media.save()

    def save(self, *args, **kwargs):
        """ Save applique les règles de validation avant l'enregistrement :
                - Vérifie les emprunts en cours.
                - Vérifie la disponibilité du média.
                - Marque le média comme non disponible si l'emprunt est actif.
        """
        if self.date_retour_effective:
            self.marquer_media_comme_disponible()
        else:
            self.verifier_disponibilite_media()
            self.verifier_nblimite_emprunts()
            self.verifier_emprunts_en_retard()
            if not self.date_emprunt:
                self.date_emprunt = timezone.now().date()
            if not self.date_retour_prevue:
                self.date_retour_prevue = self.date_emprunt + timedelta(days=7)
            self.marquer_media_comme_non_disponible()
        super().save(*args, **kwargs)
