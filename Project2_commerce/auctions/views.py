from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util
from auctions.models import *


class CreateListingForm(forms.Form):
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


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
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
                # "listings": "Listings.objects.all()"
                "listings": Listings.objects.all()
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
            util.save_listing(title, description, starting_bid,listing_image, category, added_by)
            return render(request, "auctions/index.html", {
                "listings": Listings.objects.all()
            })
    if request.method == "GET":
        return render(request, "auctions/create_listing.html",{
            "form": CreateListingForm,
        })

def listing(request,id):
    obj = Listings.objects.get(pk=id)
    added_by_user = obj.list_id_id
    return render(request, "auctions/listing.html", {
        "listing": obj,
        # "added_by": "2"
        "added_by": User.objects.values_list('username', flat=True).get(id=added_by_user)
    })
