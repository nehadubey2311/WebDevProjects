from django.urls import path
from . import views

app_name = "stocksanalyser"
urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("article/<int:article_id>", views.article, name="article"),
    path("article/category/<str:menu_item>", views.category, name="category"),
    path("article/comments/<int:article_id>", views.comments, name="comments"),
    path("article/<int:article_id>/like_unlike_article", views.like_unlike_article, name="like_unlike_article"),
    path("article/<int:article_id>/liked", views.liked, name="liked"),
]
