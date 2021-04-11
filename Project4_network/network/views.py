import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def render_with_paginator(request, all_posts, display_new_post_form=False):
    # configure pagination behavior
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/posts.html", {
        "display_new_post_form": display_new_post_form,
        "posts": all_posts,
        "page_obj": page_obj
    })

@csrf_exempt
def posts(request):
    all_posts = Post.objects.all().order_by("-created")
    return render_with_paginator(request, all_posts, True)

@csrf_exempt
@login_required
def add_post(request):
    data = json.loads(request.body)
    post = Post(user_id=request.user.id, content=data.get("content"))
    post.save()
    return JsonResponse({"message": "Post created successfully."}, status=201)

def user_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user_posts = Post.objects.filter(user=user_id)
    # Get all users current user follows
    follow_users = User.objects.values_list("follows", flat=True).filter(pk=request.user.id)
    # return True if logged in user follows the user whos profile
    # is being visited
    follows = True if user_id in follow_users else False

    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/user_profile.html", {
        "display_new_post_form": False,
        "username": user,
        "user_id": user_id,
        "posts": user_posts,
        "follows": follows,
        "page_obj": page_obj
    })

def follow(request, user_id):
    user = User.objects.get(pk=request.user.id)
    user.follows.add(user_id)
    return JsonResponse({"message": "Followed user successfully."}, status=200)

def unfollow(request, user_id):
    user = User.objects.get(pk=request.user.id)
    user.follows.remove(user_id)
    return JsonResponse({"message": "Removed followed user successfully."}, status=200)

@login_required
def following(request):
    # Get all users current user follows
    follows = User.objects.values("follows").filter(pk=request.user.id)
    # Filter all posts written by followed users
    user_posts = Post.objects.filter(user_id__in=follows)
    return render_with_paginator(request, user_posts)

@csrf_exempt
@login_required
def edit(request, post_id):
    # Get user edited post content
    data = json.loads(request.body)
    updated_content = data.get("content", "")

    # verify author is the one editing post

    # save updated post
    post = Post.objects.get(pk=post_id)
    post.content = updated_content
    post.save()

    return JsonResponse({"message": "Post updated successfully."}, status=201)

def liked(request, post_id):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    # check if logged in user has liked the post
    post = Post.objects.get(pk=post_id)
    num_likes = post.likes.count()
    print(f"num_likes is {num_likes}")
    if post.likes.filter(id=request.user.id).exists():
        return JsonResponse({"message": "liked"}, status=200)
    else:
        return JsonResponse({
            "message": "unliked",
            "likes": f"{num_likes}",
        }, status=200)
