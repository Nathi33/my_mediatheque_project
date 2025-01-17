from django.db import models


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
    name = models.fields.CharField(max_length=150)
    auteur = models.fields.CharField(max_length=250)
    disponibility = models.BooleanField(default=True, null=True, blank=True)


class Livre(Media):
    nb_pages = models.IntegerField(null=True, blank=True)


class Dvd(Media):
    genre = models.fields.CharField(max_length=250, null=True, blank=True)


class Cd(Media):
    date_sortie = models.DateField(null=True, blank=True)


class PlateauDeJeu(Media):
    nombre_joueurs_min = models.IntegerField(null=True, blank=True)
    nombre_joueurs_max = models.IntegerField(null=True, blank=True)

