from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Article, Category, Comment


class CommentForm(forms.Form):
    """
    Form to allow users enter comment on articles
    """
    comment = forms.CharField(
        label="Add a Comment",
        widget=forms.TextInput(
            attrs={"class": "form-control-file form-control-sm"}))


# Create your views here.
def index(request):
    articles = Article.objects.all()
    return render(request, "stocksanalyser/index.html", {
        "articles": articles,
    })


def login_view(request):
    """
    Logs in a user with valid username/password
    """
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("stocksanalyser:index"))
        else:
            return render(request, "stocksanalyser/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "stocksanalyser/login.html")


def logout_view(request):
    """
    Renders a logout view to user
    """
    logout(request)
    return HttpResponseRedirect(reverse("stocksanalyser:index"))


def register(request):
    """
    Registers new users to the app
    """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "stocksanalyser/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "stocksanalyser/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("stocksanalyser:index"))
    else:
        return render(request, "stocksanalyser/register.html")


def article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, "stocksanalyser/article.html",{
        "article": article,
        "comment_form": CommentForm,
        "comments": Comment.objects.filter(article=article_id)
    })


def category(request, menu_item):
    try:
        section = get_object_or_404(Category, category=menu_item)
        articles = get_list_or_404(Article, category=section.id)
        return render(request, "stocksanalyser/index.html",{
            "articles": articles,
        })
    except:
        return render(request, "stocksanalyser/banner.html", {
            "message": "Sorry no articles found under this category !!!"
        })


@login_required
def comments(request, article_id):
    """
    Adding user comments to article
    """
    # Get user id and submitted comment from form
    user = request.user.id
    comment = request.POST["comment"]

    try:
        comment = Comment(user_id=user, article_id=article_id, comment=comment)
        comment.save()
        return HttpResponseRedirect(reverse("stocksanalyser:article",
                                            args=(article_id,)))
    except:
        return render(request, "stocksanalyser/banner.html", {
            "message": "Sorry comment could not be added, \
                please try again !!"
        })


@csrf_exempt
def like_unlike_article(request, article_id):
    """
    End point to facilitate users to like/unlike an article
    """
    if request.method != "POST":
        return JsonResponse({"error": "GET request required."}, status=400)

    post = get_object_or_404(Article, pk=article_id)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user.id)
    else:
        post.likes.add(request.user.id)
    post.save()

    return JsonResponse({"message": "Article updated successfully."}, status=201)


@csrf_exempt
def liked(request, article_id):
    """Returns a status if current logged in user has
    liked an article already or not and also returns how
    many likes an article has. This end point is used to
    update all 'like' status when page loads
    Args:
        request: request received from front-end
        article_id: each article id
    Returns:
        JSON response: json response that contains message
        if an article has been liked or not by current user and
        total number of likes on that specific article
    """
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    # check if logged in user has liked the post
    article = get_object_or_404(Article, pk=article_id)
    num_likes = article.likes.count()

    if article.likes.filter(id=request.user.id).exists():
        return JsonResponse({
            "message": "liked",
            "likes": f"{num_likes}"
            }, status=200)
    else:
        return JsonResponse({
            "message": "unliked",
            "likes": f"{num_likes}",
        }, status=200)
