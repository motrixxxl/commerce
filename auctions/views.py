from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, connections
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import Bet, User, Lot

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
        if request.method == 'POST':
            new_bet = Bet()
            new_bet.lot = lot
            new_bet.amount = request.POST["bet"]
            new_bet.user = request.user
            new_bet.save()
        
        last_bet = lot.bets.order_by('-amount').first()
        next_bet_amount = lot.min_amount

        if last_bet is not None:
            next_bet_amount = last_bet.amount

    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, "auctions/lot.html", {
        "lot": lot,
        "last_bet": last_bet,
        "next_bet_amount": next_bet_amount + min_bet,
    })
