from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from app_bibliothecaire.models import Member, Book, Dvd, Cd, Board, Loan, Media
from app_bibliothecaire.forms import (Membercreation, Memberupdate, BookForm, DvdForm,
                                      CdForm, BoardForm, LoanForm, SelectBorrowerForm, ReturnLoanForm)
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import timedelta
import logging

# Création du logger
logger = logging.getLogger(__name__)


# Fonctionnalité : Menu principal
@login_required
def home_librarian(request):
    logger.info("Accès à la page d'accueil du bibliothécaire.")
    return render(request, 'app_biblio/home_bibliothecaire.html')


# Fonctionnalités : Membre
def listmembers(request):
    """ Affiche la liste des membres.
        Pour chaque membre, récupère les emprunts en cours et les inclut dans l'objet membre.
        En cas d'erreur, une redirection vers la page d'accueil est effectuée avec un message.

        Paramètres :
            - request (HttpRequest) : L'objet requête HTTP.

        Retour :
            - HttpResponse : Rendu de la page 'membres/listmembres.html' avec le contexte :
                - membres (QuerySet) : Liste des membres et leurs emprunts.
            - HttpResponseRedirect : Redirection vers la page d'accueil en cas d'erreur.
        """
    logger.info("Accès à la liste des membres.")
    try:
        members = Member.objects.all()
        for member in members:
            member.current_loans = Loan.objects.filter(borrower=member, effective_return_date__isnull=True)
            logger.debug(f"{len(members)} membres récupérés.")
            return render(request, 'membres/listmembres.html', {'members': members})
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des membres : {e}", exc_info=True)
        messages.error(request, "Erreur lors du chargement des membres.")
        return redirect('app_bibliothecaire:home_bibliothecaire')


def addmember(request):
    """ Gère l'ajout d'un nouveau membre.

        Affiche un formulaire d'ajout de membre. Si la requête est une soumission de formulaire (POST),
        elle valide les données et enregistre un nouveau membre dans la base de données. En cas d'erreur, un message
        d'erreur est affiché. Si la méthode est GET, un formulaire vide est affiché pour que l'utilisateur puisse saisir
        les informations du membre.

        Args:
            request (HttpRequest): L'objet requête HTTP.

        Returns:
            HttpResponse: La réponse contenant le rendu du formulaire d'ajout de membre ou une redirection vers la liste des membres
                          en cas de succès ou d'erreur.
        """
    logger.info("Soumission du formulaire d'ajout de membre.")
    if request.method == 'POST':
        membercreation = Membercreation(request.POST)
        if membercreation.is_valid():
            try:
                member = Member()
                member.name = membercreation.cleaned_data['name']
                member.first_name = membercreation.cleaned_data['first_name']
                member.email = membercreation.cleaned_data['email']
                member.phone = membercreation.cleaned_data['phone']
                member.save()
                logger.info(f"Membre ajouté avec succès : {member.name} {member.first_name}")
                messages.success(request, "Le membre a été mis ajouté avec succès !")
                return redirect('app_bibliothecaire:listmembres')
            except Exception as e:
                logger.error(f"Erreur lors de l'ajout du membre : {e}", exc_info=True)
                messages.error(request, "Erreur lors de l'ajout du membre.")
        else:
            logger.warning("Formulaire d'ajout de membre invalide.")
            return render(request, 'membres/ajoutmembre.html', {'memberCreation': membercreation})
    else:
        logger.info("Affichage de la page d'ajout de membre.")
        membercreation = Membercreation()
        return render(request, 'membres/ajoutmembre.html', {'memberCreation': membercreation})


def memberupdate(request, id):
    """ Permet de mettre à jour les informations d'un membre.

    Paramètres :
        - request (HttpRequest) : La requête HTTP.
        - id (int) : L'ID du membre à mettre à jour.

    Retour :
        - HttpResponse : La page du formulaire de mise à jour ou une redirection après mise à jour réussie.
    """
    member = get_object_or_404(Member, pk=id)
    if request.method == 'POST':
        member_update = Memberupdate(request.POST)
        if member_update.is_valid():
            member.name = member_update.cleaned_data['name']
            member.first_name = member_update.cleaned_data['first_name']
            member.email = member_update.cleaned_data['email']
            member.phone = member_update.cleaned_data['phone']
            member.save()
            messages.success(request, "Le membre a été mis à jour avec succès !")
        return redirect('app_bibliothecaire:listmembres')
    else:
        member_update = Memberupdate(initial={
            'name': member.name,
            'first_name': member.first_name,
            'email': member.email,
            'phone': member.phone,
        })
    return render(request, 'membres/updatemembre.html', {'memberupdate': member_update})


def memberdelete(request, id):
    """ Permet de supprimer un membre de la bibliothèque.

    Paramètres :
        - request (HttpRequest) : La requête HTTP.
        - id (int) : L'ID du membre à supprimer.

    Retour :
        - HttpResponseRedirect : Redirection vers la liste des membres après suppression.
    """
    logger.info(f"Tentative de suppression du membre avec ID : {id}")
    try:
        member = get_object_or_404(Member, pk=id)
        member.delete()
        logger.info(f"Membre supprimé avec succès : {member.name} {member.first_name}")
        messages.success(request, "Le membre a été supprimé avec succès !")
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du membre : {e}", exc_info=True)
        messages.error(request, "Erreur lors de la suppression du membre.")
    return redirect('app_bibliothecaire:listmembres')


# Fonctionnalités : Média
def listmedia(request):
    logger.info("Accès à la liste des médias.")
    try:
        books = Book.objects.all()
        dvds = Dvd.objects.all()
        cds = Cd.objects.all()
        boards = Board.objects.all()

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
        logger.debug(f"Médias récupérés : {len(books)} livres, {len(dvds)} DVD, {len(cds)} CD, {len(boards)} plateaux.")
        return render(request, 'media/listmedia.html', context)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des médias : {e}", exc_info=True)
        messages.error(request, "Erreur lors du chargement des médias.")
        return redirect('app_bibliothecaire:home_bibliothecaire')


def addmedia(request):
    return render(request, 'media/ajoutmedia.html')


def add_book(request):
    if request.method == 'POST':
        bookform = BookForm(request.POST)
        if bookform.is_valid():
            book = Book()
            book.name = bookform.cleaned_data['name']
            book.author = bookform.cleaned_data['author']
            book.availability = bookform.cleaned_data['availability']
            book.nb_pages = bookform.cleaned_data['nb_pages']
            book.category = bookform.cleaned_data['categorie']
            book.save()
            messages.success(request, "Le livre a été ajouté à la liste des médias avec succès !")
            return redirect('app_bibliothecaire:ajoutmedia')
        else:
            return render(request, 'media/ajout_livre.html', {'bookForm': bookform})
    else:
        bookform = BookForm()
        return render(request, 'media/ajout_livre.html', {'bookForm': bookform})


def add_dvd(request):
    if request.method == 'POST':
        dvdform = DvdForm(request.POST)
        if dvdform.is_valid():
            dvd = Dvd()
            dvd.name = dvdform.cleaned_data['name']
            dvd.author = dvdform.cleaned_data['author']
            dvd.availability = dvdform.cleaned_data['availability']
            dvd.genre = dvdform.cleaned_data['genre']
            dvd.category = dvdform.cleaned_data['categorie']
            dvd.save()
            messages.success(request, "Le DVD a été ajouté à la liste des médias avec succès !")
            return redirect('app_bibliothecaire:ajoutmedia')
        else:
            return render(request, 'media/ajout_dvd.html', {'dvdForm': dvdform})
    else:
        dvdform = DvdForm()
        return render(request, 'media/ajout_dvd.html', {'dvdForm': dvdform})


def add_cd(request):
    if request.method == 'POST':
        cdform = CdForm(request.POST)
        if cdform.is_valid():
            cd = Cd()
            cd.name = cdform.cleaned_data['name']
            cd.author = cdform.cleaned_data['author']
            cd.availability = cdform.cleaned_data['availability']
            cd.release_date = cdform.cleaned_data['release_date']
            cd.category = cdform.cleaned_data['categorie']
            cd.save()
            messages.success(request, "Le CD a été ajouté à la liste des médias avec succès !")
            return redirect('app_bibliothecaire:ajoutmedia')
        else:
            return render(request, 'media/ajout_cd.html', {'cdForm': cdform})
    else:
        cdform = CdForm()
        return render(request, 'media/ajout_cd.html', {'cdForm': cdform})


def add_board(request):
    if request.method == 'POST':
        boardform = BoardForm(request.POST)
        if boardform.is_valid():
            board = Board()
            board.name = boardform.cleaned_data['name']
            board.author = boardform.cleaned_data['author']
            board.number_players_min = boardform.cleaned_data['number_players_min']
            board.number_players_max = boardform.cleaned_data['number_players_max']
            board.availability = boardform.cleaned_data['availability']
            board.category = boardform.cleaned_data['categorie']
            board.save()
            messages.success(request, "Le Plateau de jeux a été ajouté à la liste des médias avec succès !")
            return redirect('app_bibliothecaire:ajoutmedia')
        else:
            return render(request, 'media/ajout_plateau.html', {'boardForm': boardform})
    else:
        boardform = BoardForm()
        return render(request, 'media/ajout_plateau.html', {'boardForm': boardform})


def create_loan(request):
    categorie = request.GET.get('categorie')
    form = LoanForm(request.GET or None, categorie=categorie)

    if request.method == 'POST':
        form = LoanForm(request.POST, categorie=categorie)
        if form.is_valid():
            try:
                borrower = form.cleaned_data['member_id']
                media = form.cleaned_data['media_id']
                loan_date = form.cleaned_data['loan_date']

                # Calculer la date de retour en fonction de la date d'emprunt
                expected_return_date = loan_date + timedelta(days=7)

                loan = Loan(borrower=borrower,
                            media=media,
                            loan_date=loan_date,
                            expected_return_date=expected_return_date)
                loan.save()

                messages.success(request, "Emprunt créé avec succès !")
                return HttpResponseRedirect(reverse('app_bibliothecaire:creer_emprunt'))
            except ValueError as e:
                messages.error(request, str(e))

    return render(request, 'emprunt/creer_emprunt.html', {'form': form})


def return_loan(request):
    # Étape 1 : Sélection de l'emprunteur
    if 'borrower_id' not in request.GET:
        if request.method == 'POST':
            form = SelectBorrowerForm(request.POST)
            if form.is_valid():
                borrower = form.cleaned_data['borrower']
                return redirect(f"{request.path}?borrower_id={borrower.id}")
        else:
            form = SelectBorrowerForm()
        return render(request, 'emprunt/select_emprunteur.html', {'form': form})

    # Étape 2 : Affichage des emprunts pour le membre sélectionné
    borrower_id = request.GET.get('borrower_id')
    borrower = get_object_or_404(Member, id=borrower_id)
    loans = Loan.objects.filter(borrower=borrower, effective_return_date__isnull=True)

    # Étape 3 : Gestion du retour d'un emprunt spécifique
    if 'loan_id' in request.GET:
        loan_id = request.GET.get('loan_id')
        loan = get_object_or_404(Loan, id=loan_id)

        if request.method == 'POST':
            form = ReturnLoanForm(request.POST)
            if form.is_valid():
                # Mise à jour des données de l'emprunt
                loan.effective_return_date = form.cleaned_data['effective_return_date']
                # Sauvegarde les données de retour
                loan.save()

                # Mise à jour de la disponibilité du média
                loan.media.availability = True
                loan.media.save()

                # Message de succès et redirection vers la liste des emprunts
                messages.success(request, f"Le retour de '{loan.media.name}' a été effectuée avec succès !")
                return redirect(reverse('app_bibliothecaire:retour_emprunt') + f"?borrower_id={borrower.id}")

        else:
            form = ReturnLoanForm(initial={
                'loan_id': loan.id,
                'media_name': loan.media.name,
                'loan_date': loan.loan_date,
                'expected_return_date': loan.expected_return_date,
            })

        return render(request, 'emprunt/retour_emprunt_detail.html', {
            'loan': loan,
            'form': form
        })

    # Affichage de la liste des emprunts pour le membre sélectionné
    return render(request, 'emprunt/retour_emprunt.html', {
        'borrower': borrower,
        'loans': loans
    })


def mediadelete(request, id):
    media = get_object_or_404(Media, pk=id)
    media.delete()
    messages.success(request, "Le media a été supprimé avec succès !")
    return redirect('app_bibliothecaire:listmedia')
