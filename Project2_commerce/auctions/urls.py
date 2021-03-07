"""Define URL(s) paths
"""
from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("addwatchlist/<int:list_id>", views.add_watchlist, name="addwatchlist"),
    path("bid/<int:list_id>", views.bid, name="bid"),
    path("category", views.category, name="category"),
    path("categorylisting/<str:category>", views.category_listing, name="categorylisting"),
    path("closelisting/<int:list_id>", views.close_listing, name="closelisting"),
    path("comments/<int:list_id>", views.comments, name="comments"),
    path("createlisting", views.create_listing, name="createlisting"),
    path("listing/<int:list_id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("removewatchlist/<int:list_id>", views.remove_watchlist, name="removewatchlist"),
    path("watchlist", views.user_watchlist, name="watchlist"),
]
