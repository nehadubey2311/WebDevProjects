from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("following", views.following, name="following"),
    path("post/<int:post_id>/edit", views.edit, name="edit"),
    path("post/<int:post_id>/like_unlike_post", views.like_unlike_post, name="like_unlike_post"),
    path("post/<int:post_id>/liked", views.liked, name="liked"),
    path("post/add_post", views.add_post, name="add_post"),
    path("profile/<int:user_id>/follow", views.follow, name="follow"),
    path("profile/<int:user_id>/unfollow", views.unfollow, name="unfollow"),
    path("profile/<int:user_id>/user_profile", views.user_profile, name="user_profile"),
]
