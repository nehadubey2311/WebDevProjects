import json

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Article, Comment, Question, User


class CommentForm(forms.ModelForm):
    """
    Form to allow users enter comment on articles
    """
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.TextInput(attrs={
                'class': 'w-100',
            })
        }


class GuestArticleForm(forms.ModelForm):
    """
    Form to let users submit guest articles
    """
    class Meta:
        model = Article
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
            })
        }


def index(request):
    """
    Render default view to users
    """
    articles = Article.objects.all().filter(approved=True).order_by("-created")
    return render_articles_with_paginator(request, articles)


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


def render_articles_with_paginator(request, articles):
    """
    This implements pagination
    Args:
        request: request as received from front-end
        articles: list of all articles to be rendered

    Returns:
        Renders all articles with paginator
    """
    # configure pagination behavior
    paginator = Paginator(articles, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # filter recommended reading articles for user
    # based on maximum likes
    articles = Article.objects.all()
    rec_readings = articles.filter(approved=True).order_by('-likes')[:5]

    return render(request, "stocksanalyser/index.html", {
        "articles": articles,
        "page_obj": page_obj,
        "rec_readings": rec_readings,
    })


def article(request, article_id):
    """
    Renders an article to the user as selected. It will
    also update if article has been like by the user or
    if user has already saved the article
    """
    saved = ""

    article = get_object_or_404(Article, pk=article_id)

    # check if user has already saved an article
    # 'saved' will have a querySet if user has saved it
    # else 'None'
    if request.user.id:
        user = User.objects.get(id=int(request.user.id))
        saved = user.watchlist.filter(id=article_id)

    return render(request, "stocksanalyser/article.html", {
        "article": article,
        "saved": saved,
        "comment_form": CommentForm,
        "comments": Comment.objects.filter(article=article_id)
    })


def category(request, menu_item):
    """
    Renders article as per menu clicked by user
    """
    try:
        articles = Article.objects.filter(
            category=menu_item).filter(approved=True).order_by("-created")
        return render_articles_with_paginator(request, articles)
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

    if not request.user.id:
        return JsonResponse({
            "error": "Only logged-in users can like/unlike articles."
        }, status=400)

    try:
        article = get_object_or_404(Article, pk=article_id)

        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user.id)
        else:
            article.likes.add(request.user.id)
        article.save()

        return JsonResponse({
            "message": "Article updated successfully."
            }, status=201)
    except:
        return JsonResponse({
            "error": "Sorry, the operation could not be completed, try again !"
        }, status=400)


@login_required
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


@login_required
def add_article(request, article_id):
    """
    This is to add an article to 'My Articles'
    """
    # Get user id for the user logged-in
    user_id = request.user.id

    try:
        article = Article.objects.get(pk=article_id)
        article.watchers.add(user_id)
        return HttpResponseRedirect(reverse("stocksanalyser:article",
                                            args=(article_id,)))
    except:
        return render(request, "stocksanalyser/banner.html", {
            "message": "Error occured, please try again..."
        })


@login_required
def remove_article(request, article_id):
    """
    This is to remove an article from 'My Articles'
    """
    # Get user id for the user logged-in
    user_id = request.user.id

    try:
        article = Article.objects.get(pk=article_id)
        article.watchers.remove(user_id)
        return HttpResponseRedirect(reverse("stocksanalyser:article",
                                            args=(article_id,)))
    except:
        return render(request, "stocksanalyser/banner.html", {
            "message": "Error occured, please try again..."
        })


@login_required
def my_articles(request):
    """
    Render user's 'My Articles'. This view re-uses
    index.html to only display watchlist articles.
    """
    articles = Article.objects.filter(watchers=request.user) \
        .filter(approved=True).order_by("-created")

    return render_articles_with_paginator(request, articles)


@login_required
def guest_article(request):
    """
    This provides the ability to users to submit an article
    to be reviewed by admin user
    """
    if request.method == "GET":
        return render(request, "stocksanalyser/guest_article.html", {
            "form": GuestArticleForm()
        })

    if request.method == "POST":
        # Accept user submitted data
        form = GuestArticleForm(request.POST)

        # validate if data is valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            category = form.cleaned_data["category"]
            added_by = request.user

            article = Article(title=title, content=content,
                              author=added_by, category=category)
            article.save()

            return HttpResponseRedirect(reverse("stocksanalyser:index"))


def user_questions(request):
    """
    This lets users submit questions on blog to be
    answered by admin user
    """
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    # fetch all questions/answers if any from DB
    entries = Question.objects.all().order_by("-created")

    return render(request, "stocksanalyser/user_questions.html", {
        "entries": entries
    })


@csrf_exempt
def submit_question(request):
    """
    Provides the ability to add user submitted questions
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    content = data.get("content")
    if not content:
        return JsonResponse({
            "error": "Empty question cannot be created."
        }, status=400)

    question = Question(user=request.user, question=content)
    question.save()

    return JsonResponse({
        "message": "Question created successfully."
        }, status=201)
