from django.urls import path
from . import views

app_name = "stocksanalyser"
urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("article/<int:article_id>", views.article, name="article"),
    path("article/<int:article_id>/add_article", views.add_article, name="add_article"),
    path("article/<int:article_id>/like_unlike_article", views.like_unlike_article, name="like_unlike_article"),
    path("article/<int:article_id>/liked", views.liked, name="liked"),
    path("article/<int:article_id>/remove_article", views.remove_article, name="remove_article"),
    path("article/category/<str:menu_item>", views.category, name="category"),
    path("article/comments/<int:article_id>", views.comments, name="comments"),
    path("articles/my_articles", views.my_articles, name="my_articles"),
    path("guest_article", views.guest_article, name="guest_article"),
    path("user_questions", views.user_questions, name="user_questions"),
]
