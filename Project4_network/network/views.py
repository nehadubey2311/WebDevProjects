import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    """
    Renders all post to users
    """
    all_posts = Post.objects.all().order_by("-created")
    return render_with_paginator(request, all_posts, True)


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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    """
    Renders a logout view to user
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
    """
    This implements pagination

    Args:
        request: request as received from front-end
        all_posts: list of all posts to be rendered
        display_new_post_form (bool, optional): Lets UI know
                     if new post form needs to be rendered or
                     not. Defaults to False.

    Returns:
        Renders all posts with/without new post form
    """
    # configure pagination behavior
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "display_new_post_form": display_new_post_form,
        "posts": all_posts,
        "page_obj": page_obj
    })


@csrf_exempt
@login_required
def add_post(request):
    """
    Provides the ability to add a new post by logged-in users
    """
    data = json.loads(request.body)
    content = data.get("content")
    if not content:
        return JsonResponse({
            "error": "Empty post cannot be created."
        }, status=400)

    post = Post(user_id=request.user.id, content=data.get("content"))
    post.save()

    return JsonResponse({"message": "Post created successfully."}, status=201)


def user_profile(request, user_id):
    """
    Renders user's profile page as per 'user_id' provided
    with all their posts
    """
    user = get_object_or_404(User, pk=user_id)
    user_posts = get_list_or_404(Post, user=user_id)
    # sorting posts reverse chronological order
    user_posts.reverse()

    # Get all users current user follows
    follow_users = User.objects.values_list(
                        "follows", flat=True).filter(pk=request.user.id)

    # return True if logged in user follows the user whos profile
    # is being visited
    is_user_followed = True if user_id in follow_users else False

    # configure pagination behavior
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # get 'followers' for a user and whom the user 'follows'
    follows = user.follows.count()
    followers = User.objects.filter(follows__in=[user_id]).count()

    return render(request, "network/user_profile.html", {
        "display_new_post_form": False,
        "username": user,
        "user_id": user_id,
        "posts": user_posts,
        "is_user_followed": is_user_followed,
        "follows": follows,
        "followers": followers,
        "page_obj": page_obj
    })


def follow(request, user_id):
    """
    End point to follow a user and save it to DB
    """
    user = get_object_or_404(User, pk=request.user.id)
    user.follows.add(user_id)
    return JsonResponse({"message": "Followed user successfully."}, status=200)


def unfollow(request, user_id):
    """
    End point to unfollow a user and update DB accordingly
    """
    user = get_object_or_404(User, pk=request.user.id)
    user.follows.remove(user_id)
    return JsonResponse({
        "message": "Removed followed user successfully."
    }, status=200)


@login_required
def following(request):
    """
    For a logged in user this renders posts for all users that
    logged in user follows
    """
    # Get all users current user follows
    follows = User.objects.values("follows").filter(pk=request.user.id)

    # Filter all posts written by followed users
    user_posts = Post.objects.filter(user_id__in=follows).order_by("-created")
    return render_with_paginator(request, user_posts)


@csrf_exempt
@login_required
def edit(request, post_id):
    """
    Provides an ability for author of posts to edit them
    """
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    # verify author is the one editing post
    post = get_object_or_404(Post, pk=post_id)
    if post.user.id != request.user.id:
        return JsonResponse({
            "error": "Only author can edit post."
        }, status=400)

    # Get user edited post content
    data = json.loads(request.body)
    updated_content = data.get("content", "")

    # save updated post
    post.content = updated_content
    post.save()

    return JsonResponse({"message": "Post updated successfully."}, status=201)


@csrf_exempt
def liked(request, post_id):
    """Returns a status if current logged in user has
    liked a post already or not and also returns how
    many likes a post has. This end point is used to
    update all posts 'like' status when page loads

    Args:
        request: request received from front-end
        post_id: each post id

    Returns:
        JSON response: json response that contains message
        if a post has been liked or not by current user and
        total number of likes on that specific post
    """
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    # check if logged in user has liked the post
    post = get_object_or_404(Post, pk=post_id)
    num_likes = post.likes.count()

    if post.likes.filter(id=request.user.id).exists():
        return JsonResponse({
            "message": "liked",
            "likes": f"{num_likes}"
            }, status=200)
    else:
        return JsonResponse({
            "message": "unliked",
            "likes": f"{num_likes}",
        }, status=200)


@csrf_exempt
def like_unlike_post(request, post_id):
    """
    End point to facilitate users to like/unlike a post
    """
    if request.method != "POST":
        return JsonResponse({"error": "GET request required."}, status=400)

    post = get_object_or_404(Post, pk=post_id)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user.id)
    else:
        post.likes.add(request.user.id)
    post.save()

    return JsonResponse({"message": "Post updated successfully."}, status=201)
