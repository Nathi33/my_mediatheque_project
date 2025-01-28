import pytest
from app_bibliothecaire.models import Membre, Media, Emprunt
from django.utils import timezone
from datetime import timedelta

# Vérifie la création d'un membre
@pytest.mark.django_db
def test_creation_membre():
    membre = Membre.objects.create(
        name='Dupont',
        first_name='Jean',
        email='jean.dupont@example.com',
        phone="0606060600",
        creation_date=timezone.now()
    )

    assert Membre.objects.count() == 1
    assert str(membre) == "Dupont Jean"


# Vérifie la création d'un média et sa disponibilité
@pytest.mark.django_db
def test_creation_media():
    media = Media.objects.create(
        name='Livre Test 1',
        auteur='Auteur Test 1',
        category='livre'
    )

    assert Media.objects.count() == 1
    assert str(media) == "Livre Test 1"
    assert media.disponibility is True


# Vérifie la création d'un emprunt et l'indisponibilité de celui-ci
@pytest.mark.django_db
def test_creation_emprunt():
    membre = Membre.objects.create(
        name='Untel',
        first_name='Truc'
    )
    media = Media.objects.create(
        name='Livre Test 2',
        auteur='Auteur Test 2',
        category='livre'
    )
    emprunt = Emprunt.objects.create(
        emprunteur=membre,
        media=media,
        date_emprunt=timezone.now()
    )

    assert Emprunt.objects.count() == 1
    assert emprunt.emprunteur == membre
    assert emprunt.media == media
    assert not media.disponibility # Le média doit être marqué comme indisponible


# Vérifie la limite des 3 emprunts actifs
@pytest.mark.django_db
def test_limite_emprunt():
    membre = Membre.objects.create(
        name='Bidule',
        first_name='Marc'
    )
    media1 = Media.objects.create(
        name='Media 1',
        auteur='Auteur 1',
        category='livre'
    )
    media2 = Media.objects.create(
        name='Media 2',
        auteur='Auteur 2',
        category='dvd'
    )
    media3 = Media.objects.create(
        name='Media 3',
        auteur='Auteur 3',
        category='cd'
    )
    media4 = Media.objects.create(
        name='Media 4',
        auteur='Auteur 4',
        category='livre'
    )

    Emprunt.objects.create(
        emprunteur=membre,
        media=media1,
        date_emprunt=timezone.now()
    )
    Emprunt.objects.create(
        emprunteur=membre,
        media=media2,
        date_emprunt=timezone.now()
    )
    Emprunt.objects.create(
        emprunteur=membre,
        media=media3,
        date_emprunt=timezone.now()
    )

    with pytest.raises(ValueError, match="Bidule Marc a déjà 3 emprunts actifs"):
        Emprunt.objects.create(
            emprunteur=membre,
            media=media4,
            date_emprunt=timezone.now()
        )


# Vérifie qu'un membre ne peut emprunter s'il a du retard
@pytest.mark.django_db
def test_retard_emprunt():
    membre = Membre.objects.create(
        name='Machin',
        first_name='Justine'
    )
    media = Media.objects.create(
        name='Media Test',
        auteur='Auteur Test',
        category='livre'
    )
    emprunt = Emprunt.objects.create(
        emprunteur=membre,
        media=media,
        date_emprunt=timezone.now() - timedelta(days=10),
        date_retour_prevue=timezone.now().date() - timedelta(days=3)
    )

    with pytest.raises(ValueError, match="Machin Justine a des emprunts en retard"):
        new_media = Media.objects.create(
            name='New Media',
            auteur='Auteur X',
            category='dvd'
        )
        Emprunt.objects.create(
            emprunteur=membre,
            media=new_media,
        date_emprunt=timezone.now()
        )


# Vérifie qu'un emprunt ne peut être créé si le média est indisponible
@pytest.mark.django_db
def test_media_non_disponible():
    membre = Membre.objects.create(
        name='Carre',
        first_name='Blanc'
    )
    media = Media.objects.create(
        name='Le Média',
        auteur='Auteur Y',
        category='livre',
        disponibility=False
    )

    with pytest.raises(ValueError, match="Le Média n'est pas disponible à l'emprunt"):
        Emprunt.objects.create(
            emprunteur=membre,
            media=media,
            date_emprunt=timezone.now()
        )



