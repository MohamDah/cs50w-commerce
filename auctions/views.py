from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, listings, biddings, winners, comments


def index(request):
    winner = winners.objects.all()
    closed = []
    for win in winner:
        closed.append(win.winner.bidded)
    listing = listings.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listing,
        "closed": closed
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

@login_required
def create(request):
    if request.method == "POST":
        name = request.user.username
        title = request.POST["title"]
        desc = request.POST["description"]
        bid = request.POST["bid"]
        if not title or not desc or not bid:
            return render(request, "auctions/create.html", {
                "message": "title, description and starting bid cannot be empty"
            })
        image = request.POST["image"]
        category = request.POST["category"]

        listing = listings(title=title, description=desc, bid=bid, image=image, category=category, seller=name)
        listing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")


def listing(request, TITLE):
    listing = listings.objects.get(pk=TITLE)
    bids = biddings.objects.filter(bidded=listing).order_by('-bid')
    winner = winners.objects.all()
    win = bids.first()
    won = False
    for winy in winner:
        if winy.winner == win:
            won = True
    if request.user.is_authenticated:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlist": request.user.watchlist.all(),
            "placed_bids": bids,
            "won": won,
            "win": win,
            "comments": comments.objects.all()
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "placed_bids": bids,
            "won": won,
            "win": win,
            "comments": comments.objects.all()
        })

@login_required
def watchlist(request):
    if request.method == "POST":
        item = listings.objects.get(pk=int(request.POST["pk"]))
        user = User.objects.get(pk=request.user.pk)
        user.watchlist.add(item)
        return HttpResponseRedirect(reverse("watchlist"))
    else:
        watchlist = request.user.watchlist.all()
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist
        })

@login_required
def remove(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.pk)
        item = listings.objects.get(pk=int(request.POST["pk"]))
        user.watchlist.remove(item)
        return HttpResponseRedirect(reverse("watchlist"))

@login_required
def bid(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.pk)
        item = listings.objects.get(pk=int(request.POST["pk"]))
        bid = int(request.POST["bid"])
        otherbids = biddings.objects.filter(bidded=item).order_by('-bid')
        if bid <= item.bid:
            return render(request, "auctions/apology.html", {
                "message": "bid is invalid (less than starting bid)",
            })

        for other in otherbids:
            if bid <= other.bid:
                return render(request, "auctions/apology.html", {
                "message": "bid is invalid (less than highest bidder)",
            })
        new = biddings(bidder=user, bidded=item, bid=bid)
        new.save()
        return HttpResponseRedirect(reverse("listing", args=(request.POST["pk"],)))

@login_required
def close(request):
    if request.method == "POST":
        item = listings.objects.get(pk=int(request.POST["pk"]))
        bids = biddings.objects.filter(bidded=item).order_by('-bid')
        if not bids:
            item.delete()
            return HttpResponseRedirect(reverse("index"))
        bid = bids.first()
        win = winners(winner=bid)
        win.save()
        return HttpResponseRedirect(reverse("listing", args=(request.POST["pk"],)))

@login_required
def comment(request):
    if request.method == "POST":
        user = request.user
        listing = listings.objects.get(pk=int(request.POST["pk"]))
        if not request.POST["comment"]:
            return render(request, "auctions/apology", {
                "message": "Comment can't be empty"
            })
        comment = request.POST["comment"]
        new_comment = comments(commenter=user, commented=listing, comment=request.POST["comment"])
        new_comment.save()
        return HttpResponseRedirect(reverse("listing", args=(request.POST["pk"],)))

def categories(request):
        category = ["digital services", "cosmetics and body care", "food and beverage", "furniture and decor", "health and wellness", "household items", "media", "pet care", "office equipment", "tools"]
        return render(request, "auctions/categories.html", {
            "categories": category
        })

def cat(request, category):
    if category == "None":
        listing = listings.objects.filter(category='')
    else:
        listing = listings.objects.filter(category=category)
    winner = winners.objects.all()
    closed = []
    for win in winner:
        closed.append(win.winner.bidded)
    return render(request, "auctions/cat.html", {
        "listings": listing,
        "closed": closed
    })

