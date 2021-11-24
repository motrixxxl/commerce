from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, connections
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from .forms import LotForm
from .models import Bid, Category, Currency, Notification, User, Lot, Watchlist, Comment

min_bid = 1

def index(request):
    return render(request, "auctions/index.html", {
        "lots": Lot.objects.filter(state=1).all(),
        "bids_notifications": getBidNotificationCount(request),
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
        last_bid = lot.bids.order_by('-amount').first()

        is_owner_last_bid = False
        if last_bid and last_bid.user.id == request.user.id:
            is_owner_last_bid = True
        next_bid_amount = lot.min_amount

        is_owner = False
        if lot.user.id == request.user.id:
            is_owner = True

        if last_bid is not None:
            next_bid_amount = last_bid.amount

        if request.user.is_authenticated:
            is_watchlisted = Watchlist.objects.filter(user=request.user, lot_id=lot_id).exists()
        else:
            is_watchlisted = True

    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, "auctions/lot.html", {
        "lot": lot,
        "comments": comments,
        "last_bid": last_bid,
        "next_bid_amount": next_bid_amount + min_bid,
        "is_watchlisted": is_watchlisted,
        "is_owner_last_bid": is_owner_last_bid,
        "is_owner": is_owner,
        "bids_notifications": getBidNotificationCount(request),
    })


@login_required(login_url='/login')
def bid(request, lot_id):
    if request.method == 'POST':
        lot = Lot.objects.get(pk=lot_id)
        if lot.user.id == request.user.id:
            return HttpResponse(status=500)
        new_bid = Bid()
        new_bid.lot = lot
        new_bid.amount = request.POST["bid"]
        new_bid.user = request.user
        new_bid.save()

    return HttpResponseRedirect(reverse('lot', kwargs={'lot_id': lot_id}))


@login_required(login_url='/login')
def addwatchlist(request, lot_id):
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
        return HttpResponse(status=500)


@login_required(login_url='/login')
def comment(request, lot_id):
    if request.method == 'POST':
        lot = Lot.objects.get(pk=lot_id)
        comment = Comment()
        comment.lot = lot
        comment.message = request.POST["message"]
        comment.user = request.user
        comment.save()

    return HttpResponseRedirect(reverse('lot', kwargs={'lot_id': lot_id}))


@login_required(login_url='/login')
def addlot(request):
    if request.method == "POST":
        form = LotForm(request.POST)
        if form.is_valid():
            lot = Lot()
            lot.user = request.user
            lot.title = request.POST['title']
            lot.image = request.POST['image']
            lot.description = request.POST['description']
            lot.category = Category.objects.get(pk=int(request.POST['category']))
            lot.min_amount = request.POST['min_amount']
            lot.currency = Currency.objects.get(pk=int(request.POST['currency']))
            lot.state = request.POST['state']
            lot.save()
            lot_id = lot.id
            return HttpResponseRedirect(reverse('lot', kwargs={'lot_id': lot_id}))
    else:
        form = LotForm()

    return render(request, 'auctions/new_lot.html', {
        "form": form,
        "bids_notifications": getBidNotificationCount(request),
    })


@login_required(login_url='/login')
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist.html', {
        "watchlist": watchlist,
        "bids_notifications": getBidNotificationCount(request),
    })


@login_required(login_url='/login')
def mylots(request):
    return render(request, 'auctions/mylots.html', {
        "lots": Lot.objects.filter(user=request.user).all(),
        "bids_notifications": getBidNotificationCount(request),
    })


@login_required(login_url='/login')
def close(request, lot_id):
    if request.method == 'POST':
        lot = Lot.objects.get(user=request.user, pk=lot_id)
        if lot is None:
            return HttpResponse(status=500)
        lot.state = 2
        lot.save()

        last_bid = lot.bids.order_by('-amount').first()
        if last_bid is not None:
            # bid is win
            last_bid.status = 1
            last_bid.save()

            notification = Notification()
            notification.user = last_bid.user
            notification.lot = lot
            # win auction
            notification.type = 1
            # notification unread
            notification.state = 1
            notification.save()

    return HttpResponseRedirect(reverse('lot', kwargs={'lot_id': lot_id}))


@login_required(login_url='/login')
def mybids(request):
    return render(request, "auctions/mybids.html", {
        "bids": Bid.objects.order_by('-created_at','lot_id','-amount').filter(user_id=request.user.id),
        "bids_notifications": getBidNotificationCount(request),
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
        "bids_notifications": getBidNotificationCount(request),
    })


def category(request, category_id):
    return render(request, "auctions/index.html", {
        "lots": Lot.objects.filter(category_id=category_id, state=1).all(),
        "bids_notifications": getBidNotificationCount(request),
    })


def getBidNotificationCount(request):
    return Notification.objects.filter(user_id=request.user.id, state=1, type=1).all().count()


def read(request):
    Notification.objects.filter(user_id=request.user.id, state=1, type=1).update(state=0)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))