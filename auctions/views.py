from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, connections
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .forms import LotForm
from .models import Bet, User, Lot, Watchlist, Comment

min_bet = 5

def index(request):
    return render(request, "auctions/index.html", {
        'lots': Lot.objects.filter(state=1).all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def lot(request, lot_id):
    try:
        lot = Lot.objects.get(pk=lot_id)
        comments = lot.comments.order_by('-created_at').all()
        last_bet = lot.bets.order_by('-amount').first()
        next_bet_amount = lot.min_amount

        if last_bet is not None:
            next_bet_amount = last_bet.amount

        if request.user.is_authenticated:
            is_watchlisted = Watchlist.objects.filter(user=request.user, lot_id=lot_id).exists()
        else:
            is_watchlisted = True

    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, "auctions/lot.html", {
        "lot": lot,
        "comments": comments,
        "last_bet": last_bet,
        "next_bet_amount": next_bet_amount + min_bet,
        "is_watchlisted": is_watchlisted,
    })


def bet(request, lot_id):
    if request.method == 'POST':
        lot = Lot.objects.get(pk=lot_id)
        new_bet = Bet()
        new_bet.lot = lot
        new_bet.amount = request.POST["bet"]
        new_bet.user = request.user
        new_bet.save()

    return HttpResponseRedirect(reverse('lot', kwargs={'lot_id': lot_id}))


def watchlist(request, lot_id):
    if request.method == 'POST':

        if request.POST["__method"] == 'PUT':
            if not Watchlist.objects.filter(user=request.user, lot_id=lot_id).exists():
                list = Watchlist()
                list.user = request.user
                list.lot = Lot.objects.get(pk=lot_id)
                list.save()
        if request.POST["__method"] == 'DELETE':
            item = Watchlist.objects.filter(user=request.user, lot_id=lot_id)
            item.delete()

        return HttpResponseRedirect(reverse('lot', kwargs={'lot_id': lot_id}))
    else:
        return render(request, 'auctions/watchlist.html')


def comment(request, lot_id):
    if request.method == 'POST':
        lot = Lot.objects.get(pk=lot_id)
        comment = Comment()
        comment.lot = lot
        comment.message = request.POST["message"]
        comment.user = request.user
        comment.save()

    return HttpResponseRedirect(reverse('lot', kwargs={'lot_id': lot_id}))


def addlot(request):
    if request.method == "POST":
        lot_id = 1
        return HttpResponseRedirect(reverse('lot', kwargs={'lot_id': lot_id}))

    return render(request, 'auctions/new_lot.html', {
        "form": LotForm,
    })