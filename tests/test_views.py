import pytest
from django.urls import reverse
from app_bibliothecaire.models import Member, Book, Media, Loan
from django.utils.timezone import now
from django.contrib.messages import get_messages
from django.test import Client
from app_bibliothecaire.forms import ReturnLoanForm

# Vérifie la création d'un membre après un POST valide
@pytest.mark.django_db
def test_add_member(client):
    response = client.post(reverse('app_bibliothecaire:ajoutmembre'), {
        'name': 'Bic',
        'first_name': 'Bleu',
        'email': 'bic.bleu@test.com',
        'phone': '0101010103'
    })

    assert response.status_code == 302
    assert Member.objects.filter(email='bic.bleu@test.com').exists()


# Vérifie la mise à jour d'un membre
@pytest.mark.django_db
def test_member_update(client):
    member = Member.objects.create(
        name="Doe",
        first_name="John",
        email="john@example.com",
        phone="123456789"
    )
    response = client.post(reverse('app_bibliothecaire:updatemembre', args=[member.id]), {
        'name': 'Doe Updated',
        'first_name': 'John',
        'email': 'john.updated@example.com',
        'phone': '9876543210'
    })
    member.refresh_from_db()
    assert member.name == "Doe Updated"
    assert member.email == 'john.updated@example.com'


# Vérifie que l'on peut supprimer un membre
@pytest.mark.django_db
def test_member_delete(client):
    member = Member.objects.create(name="Smith", first_name="Anna", email="anna@example.com", phone="123456789")
    response = client.post(reverse('app_bibliothecaire:deletemembre', args=[member.id]))
    assert response.status_code == 302
    assert not Member.objects.filter(id=member.id).exists()


# Vérifie l'ajout d'un livre
@pytest.mark.django_db
def test_add_book(client):
    response = client.post(reverse('app_bibliothecaire:ajout_livre'), {
        'name': 'Le Petit Prince',
        'author': 'Antoine de Saint-Exupéry',
        'availability': True,
        'nb_pages': 150,
        'categorie': 'book',
    })
    assert response.status_code == 302
    assert Book.objects.filter(name='Le Petit Prince').exists()


# Vérifie la suppression d'un média
@pytest.mark.django_db
def test_media_delete(client):
    media = Media.objects.create(name="Inception", availability=True)
    response = client.post(reverse('app_bibliothecaire:deletemedia', args=[media.id]))
    assert response.status_code == 302
    assert not Media.objects.filter(id=media.id).exists()


# Vérifie la création d'un emprunt
@pytest.mark.django_db
def test_create_loan(client):
    member = Member.objects.create(name="John", first_name="Doe", email="john@example.com", phone="123456")
    book = Book.objects.create(name="1984", author="George Orwell", availability=True, nb_pages=328, category="Roman")

    response = client.post(reverse('app_bibliothecaire:creer_emprunt'), {
        'member_id': member.id,
        'media_id': book.id,
        'loan_date': now().date(),
    })
    assert response.status_code == 302
    assert Loan.objects.filter(borrower=member, media=book).exists()
    book.refresh_from_db()
    assert not book.availability


# Vérifie le retour d'un emprunt et sa disponibilité
@pytest.mark.django_db
def test_return_loan(client):
    # Configuration des données initiales
    borrower = Member.objects.create(name="Test Membre")
    media = Media.objects.create(name="Test Media", availability=True)
    loan = Loan.objects.create(
        borrower=borrower,
        media=media,
        loan_date="2025-01-01",
        expected_return_date="2025-01-10",
        effective_return_date=None
    )

    # Étape 1 : Sélection de l'emprunteur
    response = client.get(reverse('app_bibliothecaire:retour_emprunt'))
    assert response.status_code == 200
    assert "Sélectionner un emprunteur" in response.content.decode()

    # Simuler la sélection de l'emprunteur
    response = client.post(reverse('app_bibliothecaire:retour_emprunt'), {
        'borrower': borrower.id
    })
    assert response.status_code == 302
    assert f"borrower_id={borrower.id}" in response.url

    # Étape 2 : Affichage des emprunts pour l'emprunteur
    response = client.get(response.url)
    assert response.status_code == 200
    assert loan in response.context['loans']

    # Étape 3 : Retour de l'emprunt
    response = client.post(
        reverse('app_bibliothecaire:retour_emprunt') + f"?borrower_id={borrower.id}&loan_id={loan.id}", {
            'effective_return_date': "2025-01-15",
            'loan_id': loan.id
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




