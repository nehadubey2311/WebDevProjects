from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.db import models
import re
import markdown2
import random

from . import util


class AddPageForm(forms.Form):
    formData = forms.CharField(label="Page Title")
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'rows':5,'cols':20}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "header": "All Pages",
        "entries": util.list_entries()
    })

def searchString(request):
    if request.method == "POST":
        # accept user input string and find entry if exists
        searchString = request.POST.get('q')
        if util.get_entry(searchString):
            return HttpResponseRedirect(reverse('encyclopedia:wikipages', \
                kwargs={'pageTitle':searchString}))
        else:
            # find entries that match with keyword entered by making case insensitive search
            entries = util.list_entries()
            patternMatch = [entry for entry in entries if re.search(searchString, entry, re.IGNORECASE)]
            return render(request, "encyclopedia/index.html", {
                "header": "Search Results",
                "entries": patternMatch
            })

def wikiPage(request, pageTitle):
    try:
        return render(request, "encyclopedia/wikiPage.html", {
            "content": markdown2.markdown(util.get_entry(pageTitle)),
            "title": pageTitle
        })
    except:
        return render(request, "encyclopedia/errorPage.html", {
            "errorMsg": "The requested page was not found !!"
        })

def addPage(request):
    if request.method == "POST":
        # Accept user submitted date
        form = AddPageForm(request.POST)
        # validate if data is valid
        if form.is_valid():
            title = form.cleaned_data["formData"]
            content = form.cleaned_data["content"]
            # Save new page if entry does not already exist
            if not util.get_entry(title):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('encyclopedia:wikipages', kwargs={'pageTitle':title}))
            else:
                return render(request, "encyclopedia/errorPage.html", {
                    "errorMsg": "The entry already exists"
                })
        else:
            return HttpResponse("Form had invalid data...try again...") 

    if request.method == "GET":
        return render(request, "encyclopedia/addPage.html", {
            "form": AddPageForm()
        })

def editPage(request, title):
    if request.method == "GET":
        return render(request, "encyclopedia/addPage.html", {
                "form": AddPageForm({
                    'formData':'sample title', 
                    'content': util.get_entry(title)
                })
            })

def randomPage(request):
    entryList = util.list_entries()
    randomSelection = random.choice(entryList)
    return render(request, "encyclopedia/wikiPage.html", {
        "content": markdown2.markdown(util.get_entry(randomSelection)),
        "title": randomSelection
    }) 
    