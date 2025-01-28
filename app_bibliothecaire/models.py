from django.db import models
from django.utils import timezone
from datetime import timedelta


class Membre(models.Model):
    name = models.fields.CharField(max_length=150)
    first_name = models.fields.CharField(max_length=150)
    # Autorise la valeur NULL dans la BDD et permet de ne pas renseigner le champ dans le formulaire
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    creation_date = models.DateTimeField(
        default=timezone.now)  # La date sera enregistrée avec le fuseau horaire configuré

    # La méthode str définit la représentation textuelle de l'objet.
    # Elle permet la lisibilité dans l'administration Django,
    # facilite l'identification lors du débogage
    # et permet la clarté dans les relations entre modèles.
    def __str__(self):
        return f"{self.name} {self.first_name}"


class Media(models.Model):
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
    emprunteur = models.ForeignKey(
        Membre,  # Relation vers la classe Membre
        on_delete=models.CASCADE,  # Supprime l'emprunt si le membre est supprimé
        related_name="emprunts"  # Permet de retrouver ts les emprunts d'un membre via membre.emprunts.all()
    )
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="emprunts"  # Permet de retrouver tous les emprunts pour un média
    )
    date_emprunt = models.DateTimeField(null=True, blank=True)
    # L'argument default permet de préciser une valeur par défaut si l'utilisateur n'en fournit pas,
    # lamba est une fonction pour calculer la date de retour prévue au moment de la création de l'emprunt,
    # now() renvoie la date et l'heure actuelle et date() extrait uniquement la date sans l'heure,
    # en ajoutant timedelta() à la date actuelle, o, obtient un delta de 7jours.
    date_retour_prevue = models.DateField(default=get_default_date_emprunt)
    date_retour_effective = models.DateField(null=True, blank=True)

    # Représentation textuelle d'un objet
    def __str__(self):
        # f indique qu'il s'agit d'une f-string (manière de formater du texte en Python)
        # self.media représente la relation entre l'emprunt et le média via la clé étrangère ForeignKey
        # .name accède au champ name du modèle Media correspondant au nom du média emprunté
        # self.emprunteur renvoie la représentation textuelle de l'emprunteur définit dans la méthode __str__ du modèle Membre
        return f"{self.media.name} emprunté par {self.emprunteur}"

    def verifier_nblimite_emprunts(self):
        # Emprunt.objects.filter(...) : requête filtrant les objets Emprunt remplissant certaines conditions
        emprunts_actifs = Emprunt.objects.filter(
            # Sélection uniquement des emprunts associés à l'emprunteur actuel
            emprunteur=self.emprunteur,
            # Filtre uniquement les emprunts n'ayant pas encore de date de retour effective
            date_retour_effective__isnull=True
            # Cette méthode comte le nombre d'éléments retournés par la requête
        ).count()
        # Si le nb d'emprunts est > ou = à 3
        if emprunts_actifs >= 3:
            # Si le membre a atteint ou dépassé la limite de 3 emprunts actifs alors une exception ValueError est levée
            # et un message d'erreur apparait indiquant le problème.
            # Une exception est un mécanisme interrompant l'exécution normale d'un programme
            # lorsqu'un évènement inattendu se produit
            raise ValueError(f"{self.emprunteur} a déjà 3 emprunts actifs")

    # Vérifie si le membre a des emprunts en retard
    def verifier_emprunts_en_retard(self):
        emprunts_en_retard = Emprunt.objects.filter(
            emprunteur=self.emprunteur,
            # Vérifie que le média n'a pas encore été rendu
            date_retour_effective__isnull=True,
            # Compare la date de retour prévue et la date actuelle
            # now().date() récupère la date du jour
            # lt signifie inférieur à
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
        # self : fait référence à l'instance actuelle de l'objet du modèle
        # *args : permet de passer un nombre variable d'arguments non nommés
        # **kwargs : permet de passer un nombre variable d'arguments nommés
        # Si c'est un retour
        if self.date_retour_effective:
            self.marquer_media_comme_disponible()
        else:
            # Vérification des règles avant d'enregistrer l'emprunt
            self.verifier_disponibilite_media()
            self.verifier_nblimite_emprunts()
            self.verifier_emprunts_en_retard()
            # Définit la date d'emprunt si elle n'est pas spécifiée
            if not self.date_emprunt:
                self.date_emprunt = timezone.now().date()
            # Définit la date de retour prévue si elle n'est pas spécifiée
            if not self.date_retour_prevue:
                self.date_retour_prevue = self.date_emprunt + timedelta(days=7)
            self.marquer_media_comme_non_disponible()
        super().save(*args, **kwargs)  # Appel de la méthode save() parente
