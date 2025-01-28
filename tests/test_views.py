import pytest
from django.urls import reverse
from app_bibliothecaire.models import Membre, Livre, Media, Emprunt
from django.utils.timezone import now
from django.contrib.messages import get_messages
from django.test import Client
from app_bibliothecaire.forms import RetourEmpruntForm

# Vérifie la création d'un membre après un POST valide
@pytest.mark.django_db
def test_ajout_membre(client):
    response = client.post(reverse('app_bibliothecaire:ajoutmembre'), {
        'name': 'Bic',
        'first_name': 'Bleu',
        'email': 'bic.bleu@test.com',
        'phone': '0101010103'
    })

    assert response.status_code == 302
    assert Membre.objects.filter(email='bic.bleu@test.com').exists()


# Vérifie la mise à jour d'un membre
@pytest.mark.django_db
def test_update_membre(client):
    membre = Membre.objects.create(
        name="Doe",
        first_name="John",
        email="john@example.com",
        phone="123456789"
    )
    response = client.post(reverse('app_bibliothecaire:updatemembre', args=[membre.id]), {
        'name': 'Doe Updated',
        'first_name': 'John',
        'email': 'john.updated@example.com',
        'phone': '9876543210'
    })
    membre.refresh_from_db()
    assert membre.name == "Doe Updated"
    assert membre.email == "john.updated@example.com"


# Vérifie que l'on peut supprimer un membre
@pytest.mark.django_db
def test_delete_membre(client):
    membre = Membre.objects.create(name="Smith", first_name="Anna", email="anna@example.com", phone="123456789")
    response = client.post(reverse('app_bibliothecaire:deletemembre', args=[membre.id]))
    assert response.status_code == 302
    assert not Membre.objects.filter(id=membre.id).exists()


# Vérifie l'ajout d'un livre
@pytest.mark.django_db
def test_ajout_livre(client):
    response = client.post(reverse('app_bibliothecaire:ajout_livre'), {
        'name': 'Le Petit Prince',
        'auteur': 'Antoine de Saint-Exupéry',
        'disponibility': True,
        'nb_pages': 150,
        'categorie': 'livre',
    })
    assert response.status_code == 302
    assert Livre.objects.filter(name='Le Petit Prince').exists()


# Vérifie la suppression d'un média
@pytest.mark.django_db
def test_delete_media(client):
    media = Media.objects.create(name="Inception", disponibility=True)
    response = client.post(reverse('app_bibliothecaire:deletemedia', args=[media.id]))
    assert response.status_code == 302
    assert not Media.objects.filter(id=media.id).exists()


# Vérifie la création d'un emprunt
@pytest.mark.django_db
def test_creer_emprunt(client):
    membre = Membre.objects.create(name="John", first_name="Doe", email="john@example.com", phone="123456")
    livre = Livre.objects.create(name="1984", auteur="George Orwell", disponibility=True, nb_pages=328, category="Roman")

    response = client.post(reverse('app_bibliothecaire:creer_emprunt'), {
        'membre_id': membre.id,
        'media_id': livre.id,
        'date_emprunt': now().date(),
    })
    assert response.status_code == 302
    assert Emprunt.objects.filter(emprunteur=membre, media=livre).exists()
    livre.refresh_from_db()
    assert not livre.disponibility


# Vérifie le retour d'un emprunt et sa disponibilité
@pytest.mark.django_db
def test_retour_emprunt(client):
    # Configuration des données initiales
    emprunteur = Membre.objects.create(name="Test Membre")
    media = Media.objects.create(name="Test Media", disponibility=True)
    emprunt = Emprunt.objects.create(
        emprunteur=emprunteur,
        media=media,
        date_emprunt="2025-01-01",
        date_retour_prevue="2025-01-10",
        date_retour_effective=None
    )

    # Étape 1 : Sélection de l'emprunteur
    response = client.get(reverse('app_bibliothecaire:retour_emprunt'))
    assert response.status_code == 200
    assert "Sélectionner un emprunteur" in response.content.decode()

    # Simuler la sélection de l'emprunteur
    response = client.post(reverse('app_bibliothecaire:retour_emprunt'), {
        'emprunteur': emprunteur.id
    })
    assert response.status_code == 302
    assert f"emprunteur_id={emprunteur.id}" in response.url

    # Étape 2 : Affichage des emprunts pour l'emprunteur
    response = client.get(response.url)
    assert response.status_code == 200
    assert emprunt in response.context['emprunts']

    # Étape 3 : Retour de l'emprunt
    response = client.post(
        reverse('app_bibliothecaire:retour_emprunt') + f"?emprunteur_id={emprunteur.id}&emprunt_id={emprunt.id}", {
            'date_retour_effective': "2025-01-15",
            'emprunt_id': emprunt.id
        })

    # Vérification de la réponse
    if response.status_code == 200:
        print(response.content.decode())  # Pour afficher le contenu et comprendre pourquoi ce n'est pas une redirection.
    assert response.status_code == 302


# Vérifie l'authentification
@pytest.mark.django_db
def test_access_home_bibliothecaire_unauthenticated(client):
    response = client.get(reverse('app_bibliothecaire:home_bibliothecaire'))
    assert response.status_code == 302  # Redirection vers la page de login
    assert '/login/' in response.url