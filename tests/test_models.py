import pytest
from app_bibliothecaire.models import Member, Media, Loan
from django.utils import timezone
from datetime import timedelta


# Vérifie la création d'un membre
@pytest.mark.django_db
def test_member_creation():
    member = Member.objects.create(
        name='Dupont',
        first_name='Jean',
        email='jean.dupont@example.com',
        phone="0606060600",
        creation_date=timezone.now()
    )

    assert Member.objects.count() == 1
    assert str(member) == "Dupont Jean"


# Vérifie la création d'un média et sa disponibilité
@pytest.mark.django_db
def test_media_creation():
    media = Media.objects.create(
        name='Livre Test 1',
        author='Auteur Test 1',
        category='livre'
    )

    assert Media.objects.count() == 1
    assert str(media) == "Livre Test 1"
    assert media.availability is True


# Vérifie la création d'un emprunt et l'indisponibilité de celui-ci
@pytest.mark.django_db
def test_loan_creation():
    member = Member.objects.create(
        name='Untel',
        first_name='Truc'
    )
    media = Media.objects.create(
        name='Livre Test 2',
        author='Auteur Test 2',
        category='livre'
    )
    loan = Loan.objects.create(
        borrower=member,
        media=media,
        loan_date=timezone.now()
    )

    assert Loan.objects.count() == 1
    assert loan.borrower == member
    assert loan.media == media
    assert not media.availability # Le média doit être marqué comme indisponible


# Vérifie la limite des 3 emprunts actifs
@pytest.mark.django_db
def test_borrowing_limit():
    member = Member.objects.create(
        name='Bidule',
        first_name='Marc'
    )
    media1 = Media.objects.create(
        name='Media 1',
        author='Auteur 1',
        category='livre'
    )
    media2 = Media.objects.create(
        name='Media 2',
        author='Auteur 2',
        category='dvd'
    )
    media3 = Media.objects.create(
        name='Media 3',
        author='Auteur 3',
        category='cd'
    )
    media4 = Media.objects.create(
        name='Media 4',
        author='Auteur 4',
        category='livre'
    )

    Loan.objects.create(
        borrower=member,
        media=media1,
        loan_date=timezone.now()
    )
    Loan.objects.create(
        borrower=member,
        media=media2,
        loan_date=timezone.now()
    )
    Loan.objects.create(
        borrower=member,
        media=media3,
        loan_date=timezone.now()
    )

    with pytest.raises(ValueError, match="Bidule Marc a déjà 3 emprunts actifs"):
        Loan.objects.create(
            borrower=member,
            media=media4,
            loan_date=timezone.now()
        )


# Vérifie qu'un membre ne peut emprunter s'il a du retard
@pytest.mark.django_db
def test_late_loans():
    member = Member.objects.create(
        name='Machin',
        first_name='Justine'
    )
    media = Media.objects.create(
        name='Media Test',
        author='Auteur Test',
        category='livre'
    )
    loan = Loan.objects.create(
        borrower=member,
        media=media,
        loan_date=timezone.now() - timedelta(days=10),
        expected_return_date=timezone.now().date() - timedelta(days=3)
    )

    with pytest.raises(ValueError, match="Machin Justine a des emprunts en retard"):
        new_media = Media.objects.create(
            name='New Media',
            author='Auteur X',
            category='dvd'
        )
        Loan.objects.create(
            borrower=member,
            media=new_media,
            loan_date=timezone.now()
        )


# Vérifie qu'un emprunt ne peut être créé si le média est indisponible
@pytest.mark.django_db
def test_media_as_unavailable():
    member = Member.objects.create(
        name='Carre',
        first_name='Blanc'
    )
    media = Media.objects.create(
        name='Le Média',
        author='Auteur Y',
        category='livre',
        availability=False
    )

    with pytest.raises(ValueError, match="Le Média n'est pas disponible à l'emprunt"):
        Loan.objects.create(
            borrower=member,
            media=media,
            loan_date=timezone.now()
        )

