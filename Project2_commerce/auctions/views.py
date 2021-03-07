"""
Python function that takes a Web request
and returns a Web response
"""

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auctions.models import Bid, Category, Comment, Listing, User

from . import util


class CreateListingForm(forms.Form):
    """
    Class to create a
    'Listings' form
    """
    title = forms.CharField(
        label="Listing Title",
        widget=forms.TextInput(
            attrs={"class": "form-control-file form-control-sm"}))
    description = forms.CharField(
        label="Listing Description",
        widget=forms.Textarea(
            attrs={"class": "form-control form-control-sm"}))
    starting_bid = forms.CharField(
        label="Starting Bid",
        widget=forms.TextInput(
            attrs={"class": "form-control-file form-control-sm"}))
    listing_image = forms.CharField(
        label="Listing Image URL",
        widget=forms.TextInput(
            attrs={"class": "form-control-file form-control-sm"}))
    category = forms.CharField(
        label="Listing Category",
        widget=forms.Select(
            choices=Category.objects.values_list(),
            attrs={"class": "form-control-file form-control-sm"}))


class CommentForm(forms.Form):
    """
    Form to allow users enter comment on listings
    """
    comment = forms.CharField(
        label="Add a Comment",
        widget=forms.TextInput(
            attrs={"class": "form-control-file form-control-sm"}))


def index(request):
    """
    Render the default page with
    all listings
    """
    # Use complex lookup with Q object to check if listing is active
    # or listing has been won by requesting user, only then display it
    user = request.user.id
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(Q(is_active=True) | Q(winner=user))
    })


def login_view(request):
    """
    To render login view to user
    """
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render(request, "auctions/index.html", {
                "listings": Listing.objects.filter(Q(is_active=True) |
                                                   Q(winner=request.user.id))
            })
        return render(request, "auctions/login.html", {
            "message": "Invalid username and/or password."
        })
    return render(request, "auctions/login.html")


def logout_view(request):
    """
    Render logout view
    """
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    """
    Register a new user
    """
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
    return render(request, "auctions/register.html")


def create_listing(request):
    """
    Create a new listing
    """
    if request.method == "POST":
        # Accept user submitted data
        form = CreateListingForm(request.POST)

        # validate if data is valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            listing_image = form.cleaned_data["listing_image"]
            category = form.cleaned_data["category"]
            added_by = request.user.id

            # try saving listing
            try:
                util.save_listing(title, description, starting_bid,

                                  listing_image, category, added_by)
                return render(request, "auctions/index.html", {
                    "listings": Listing.objects.filter(
                                Q(is_active=True) |
                                Q(winner=request.user.id))
                })
            except ValueError:
                return render(request, "auctions/message_banner.html", {
                    "message": "The values entered were not correct,\
                      please try again..."
                })

    # Render create listing form if request was GET
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {
            "form": CreateListingForm,
        })


def listing(request, list_id):
    """
    Display details for a specific listing
    identified by listing id
    """
    if request.method == "GET":
        obj = Listing.objects.get(pk=list_id)
        added_by_user = obj.user_id
        watcher = ""

        # check if user is already watching a listing
        # 'watcher' will return a querySet if user is a watcher
        # else 'none'
        if request.user.id:
            user = User.objects.get(id=int(request.user.id))
            watcher = user.watchlist.filter(id=list_id)

        return render(request, "auctions/listing.html", {
            "listing": obj,
            "added_by": User.objects.values_list(
                        "username", flat=True).get(id=added_by_user),
            "watcher": watcher,
            "comment_form": CommentForm,
            "comments": Comment.objects.filter(listing=list_id),
            "category": Category.objects.values_list(
                        "category", flat=True).get(pk=obj.category.id)
        })
    return None


def bid(request, list_id):
    """
    Add bid for a listing
    """
    if request.method == "POST":
        try:
            # Get current and user submitted bid to compare
            current_bid = Listing.objects.get(pk=list_id).bid
            user_bid = int(request.POST["bid"])

            if not user_bid > current_bid:
                return render(request, "auctions/message_banner.html", {
                    "message": "Bid amount entered was lower than last bid, \
                                please try again !!"
                })

            # Try saving user bid to bid model
            util.save_bid(list_id, request.user.id,
                          user_bid, current_bid)
            return HttpResponseRedirect(reverse("auctions:listing",
                                                args=(list_id,)))
        except ValueError:
            return render(request, "auctions/message_banner.html", {
                "message": "Bid amount entered was not valid, \
                            please try again !!"
            })
    return None


def watchlist(request, list_id):
    """
    This is to add a Listing to user's watchlist
    """
    # Get user id for the user logged-in
    user_id = request.user.id

    try:
        util.add_to_watchlist(list_id, user_id)
        return HttpResponseRedirect(reverse("auctions:listing",
                                            args=(list_id,)))
    except:
        return render(request, "auctions/message_banner.html", {
            "message": "Error occured, please try again..."
        })


def remove_watchlist(request, list_id):
    """
    Remove a listing from watchlist
    """
    # Get user id for the user logged-in
    user_id = request.user.id

    try:
        util.remove_from_watchlist(list_id, user_id)
        return HttpResponseRedirect(reverse("auctions:listing",
                                            args=(list_id,)))
    except:
        return render(request, "auctions/message_banner.html", {
            "message": "Error occured, please try again..."
        })


def close_listing(request, list_id):
    """
    Close the listing.
    Identify and assign winner for the listing
    """
    try:
        user = Bid.objects.get(listing=list_id).user
    # if we reached 'except' that would indicate there was no
    # bid for the listing and the owner of the listing is
    # the highest bidder, hence they win listing
    except:
        user = request.user

    try:
        util.close_listing(list_id, user)
        return render(request, "auctions/index.html", {
                "listings": Listing.objects.filter(Q(is_active=True) |
                                                   Q(winner=request.user.id))
        })
    except:
        return render(request, "auctions/message_banner.html", {
            "message": "Some error occured, please try again !!"
        })


def comments(request, list_id):
    """
    Adding user comments to listing
    """
    if request.method == "POST":
        # Get user id and submitted comment from form
        user = request.user.id
        comment = request.POST["comment"]

        try:
            util.save_comment(list_id, user, comment)
            return HttpResponseRedirect(reverse("auctions:listing",
                                                args=(list_id,)))
        except:
            return render(request, "auctions/message_banner.html", {
                "message": "Sorry comment could not be added, \
                    please try again !!"
            })

    return None


def user_watchlist(request):
    """
    Render a user's watchlist. This view re-uses
    index.html to only display watchlist items.
    """
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(watchers=request.user)
    })


def category(request):
    """
    Display all categories to user as a list
    """
    try:
        categories = Category.objects.values_list()

        # 'categories' return a tuple, extract category values
        category = [row[1] for row in categories]

        return render(request, "auctions/categories.html", {
            "categories": category
        })
    except:
        return render(request, "auctions/message_banner.html", {
                "message": "Sorry categories could not be retrieved, \
                    please try again !!"
            })


def category_listing(request, category):
    """
    Display listings that belong to a specific category
    """
    category_id = Category.objects.get(category=category)

    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=category_id.id).
        filter(Q(is_active=True) | Q(winner=request.user.id))
    })
