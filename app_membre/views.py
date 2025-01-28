from django.shortcuts import render
from app_bibliothecaire.models import Book, Dvd, Cd, Board


def member_home(request):
    return render(request, 'app_memb/home_membre.html')


def list_medias_member(request):
    # Recharge les médias depuis la BDD pour afficher l'état actuel
    books = Book.objects.all()
    dvds = Dvd.objects.all()
    cds = Cd.objects.all()
    boards = Board.objects.all()

    # Permet la prise en compte d'un emprunt en cours
    for book in books:
        book.current_loans = book.loans.filter(effective_return_date__isnull=True).first()
    for dvd in dvds:
        dvd.current_loans = dvd.loans.filter(effective_return_date__isnull=True).first()
    for cd in cds:
        cd.current_loans = cd.loans.filter(effective_return_date__isnull=True).first()

    context = {
        'books': books,
        'dvds': dvds,
        'cds': cds,
        'boards': boards,
    }
    return render(request, 'app_memb/liste_medias_membre.html', context)
