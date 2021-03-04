from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auctions.models import User, Listing, Bid, Comment
from . import util


class CreateListingForm(forms.Form):
    """Class to create a
    'Listings' form
    """
    title = forms.CharField(
        label="Listing Title",
        widget=forms.TextInput(
            attrs={'class': 'form-control-file form-control-sm'}))
    description = forms.CharField(
        label="Listing Description",
        widget=forms.Textarea(
            attrs={'class': 'form-control form-control-sm'}))
    starting_bid = forms.CharField(
        label="Starting Bid",
        widget=forms.TextInput(
            attrs={'class': 'form-control-file form-control-sm'}))
    listing_image = forms.CharField(
        label="Listing Image URL",
        widget=forms.TextInput(
            attrs={'class': 'form-control-file form-control-sm'}))
    category = forms.CharField(
        label="Listing Category",
        widget=forms.TextInput(
            attrs={'class': 'form-control-file form-control-sm'}))


class CommentForm(forms.Form):
    """[summary]
    Form to allow users enter comment on listings
    """
    comment = forms.CharField(
        label="Add a Comment",
        widget=forms.TextInput(
            attrs={'class': 'form-control-file form-control-sm'}))

def index(request):
    # Use complex lookup with Q object to check if listing is active
    # or listing has been won by requesting user, only then display it
    user = request.user.id
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(Q(is_active=True) | Q(winner=user))
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
            return render(request, "auctions/index.html", {
                "listings": Listing.objects.filter(is_active=True)
            })
            # return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        # Accept user submitted date
        form = CreateListingForm(request.POST)
        # validate if data is valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            listing_image = form.cleaned_data["listing_image"]
            category = form.cleaned_data["category"]
            added_by = request.user
            util.save_listing(title, description, starting_bid, listing_image, category, added_by)
            return render(request, "auctions/index.html", {
                "listings": Listing.objects.filter(is_active=True)
            })
    if request.method == "GET":
        return render(request, "auctions/create_listing.html",{
            "form": CreateListingForm,
        })

def listing(request, list_id):
    if request.method == "GET":
        obj = Listing.objects.get(pk=list_id)
        added_by_user = obj.user_id
        # check if user is already watching a listing
        # 'watcher' will return a querySet if user is a watcher
        # else none
        user = User.objects.get(id=int(request.user.id))
        watcher = user.watchlist.filter(id=list_id)
        return render(request, "auctions/listing.html", {
            "listing": obj,
            "added_by": User.objects.values_list('username', flat=True).get(id=added_by_user),
            "watcher": watcher,
            "commentForm": CommentForm,
            "comments": Comment.objects.filter(listing=list_id)
        })


def bid(request, list_id):
    if request.method == "POST":
        bid = Listing.objects.get(pk=list_id).starting_bid
        start_bid = Listing.objects.get(pk=list_id).starting_bid
        try:
            util.save_bid(list_id, request.user.id, int(request.POST["bid"]), start_bid)
            return HttpResponseRedirect(reverse("auctions:listing", args=(list_id,)))
        except:
            return render(request, "auctions/message_banner.html", {
                "message": "Bid amount entered was lower than last bid, please try again !!"
            })

def watchlist(request, list_id):
    """[summary]
    This is to add a Listing to user's watchlist
    """
    user_id = request.user.id
    try:
        util.add_to_watchlist(list_id, user_id)
        return HttpResponseRedirect(reverse("auctions:listing", args=(list_id,)))
    except:
        return render(request, "auctions/message_banner.html", {
            "message": "Error occured, please try again..."
        })

def remove_watchlist(request, list_id):
    user_id = request.user.id
    try:
        util.remove_from_watchlist(list_id, user_id)
        return HttpResponseRedirect(reverse("auctions:listing", args=(list_id,)))
    except:
        return render(request, "auctions/message_banner.html", {
            "message": "Error occured, please try again..."
        })

def close_listing(request, list_id):
    """[summary]
    Close the listing.
     
    Identify and assign winner for the listing
    if there was no bid on the listing then creater
    of the listing 'wins' it
    """
    try:
        user = Bid.objects.get(listing=list_id).user
    except:
        user = request.user
    try:
        util.close_listing(list_id, user)
        return HttpResponseRedirect(reverse("auctions:listing", args=(list_id,)))
    except:
        return render(request, "auctions/message_banner.html", {
            "message": "Some error occured, please try again !!"
        })

def comments(request, list_id):
    if request.method == "POST":
        user = request.user.id
        comment = request.POST["comment"]
        try:
            util.save_comment(list_id, user, comment)
            return HttpResponseRedirect(reverse("auctions:listing", args=(list_id,)))
        except: 
            return render(request, "auctions/message_banner.html", {
                "message": "Sorry comment could not be added, please try again !!"
            })

def user_watchlist(request):
    """[summary]
    Render a user's watchlist. This view reuses
    index.html to only display watchlist items.
    """
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(watchers=request.user)
    })
