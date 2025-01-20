from django.db import models
from django.utils.timezone import now
from datetime import timedelta


class Membre(models.Model):
    name = models.fields.CharField(max_length=150)
    first_name = models.fields.CharField(max_length=150)
    # Autorise la valeur NULL dans la BDD et permet de ne pas renseigner le champ dans le formulaire
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True) #Définit automatiquement la date et l'heure à la création

    #La méthode str définit la représentation textuelle de l'objet.
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


def get_default_date_emprunt(date_emprunt):
    # Calcule la date de retour prévue en fonction de la date d'emprunt
    return date_emprunt + timedelta(days=7)


class Emprunt(models.Model):
    emprunteur = models.ForeignKey(
        Membre, #Relation vers la classe Membre
        on_delete=models.CASCADE, #Supprime l'emprunt si le membre est supprimé
        related_name="emprunts" #Permet de retrouver ts les emprunts d'un membre via membre.emprunts.all()
    )
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="emprunts" #Permet de retrouver tous les emprunts pour un média
    )
    date_emprunt = models.DateTimeField(null=True, blank=True)
    #L'argument default permet de préciser une valeur par défaut si l'utilisateur n'en fournit pas,
    #lamba est une fonction pour calculer la date de retour prévue au moment de la création de l'emprunt,
    #now() renvoie la date et l'heure actuelle et date() extrait uniquement la date sans l'heure,
    #en ajoutant timedelta() à la date actuelle, o, obtient un delta de 7jours.
    date_retour_prevue = models.DateField(default=get_default_date_emprunt)
    date_retour_effective = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Si c'est un retour (date_retour_effective non nulle)
        if self.date_retour_effective:
            # Marque le média comme disponible lors du retour
            self.media.disponibility = True
            self.media.save()
        else:
            #Vérifie que le média n'est pas un plateau de jeu
            if isinstance(self.media, Plateau):
                raise ValueError("les Plateaux de jeux ne peuvent pas être empruntés.")

            #Vérifie que le membre n'a pas 3 emprunts actifs
            emprunts_actifs = Emprunt.objects.filter(
                emprunteur=self.emprunteur,
                date_retour_effective__isnull=True
            ).count()
            if emprunts_actifs >= 3:
                raise ValueError(f"{self.emprunteur} a déjà 3 emprunts actifs.")

            #Vérifie si le membre a des emprunts en retard
            emprunts_en_retard = Emprunt.objects.filter(
                emprunteur=self.emprunteur,
                date_retour_effective__isnull=True,
                date_retour_prevue__lt=now().date()
            )
            if emprunts_en_retard.exists():
                raise ValueError(f"{self.emprunteur} a des emprunts en retard et ne peut pas emprunter de nouveaux médias.")

            #Vérifie que le média est disponible
            if not self.media.disponibility:
                raise ValueError(f"{self.media.name} n'est pas disponible à l'emprunt.")

            #Marque le média comme non disponible
            self.media.disponibility = False
            self.media.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.media.name} emprunté par {self.emprunteur}"

