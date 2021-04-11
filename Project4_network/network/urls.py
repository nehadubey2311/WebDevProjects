from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("following", views.following, name="following"),
    path("post/add", views.add_post, name="add"),
    path("posts", views.posts, name="posts"),
    path("post/<int:post_id>/edit", views.edit, name="edit"),
    path("post/<int:post_id>/liked", views.liked, name="liked"),
    path("profile/<int:user_id>", views.user_profile, name="profile"),
    path("profile/<int:user_id>/follow", views.follow, name="follow"),
    path("profile/<int:user_id>/unfollow", views.unfollow, name="unfollow"),
]
