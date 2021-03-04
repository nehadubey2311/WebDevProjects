"""Define URL(s) paths
"""
from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="create_listing"),
    path("listing/<int:list_id>", views.listing, name="listing"),
    path("<int:list_id>/bid", views.bid, name="bid"),
    path("watchlist/<int:list_id>", views.watchlist, name="watchlist"),
    path("remove_watchlist/<int:list_id>", views.remove_watchlist, name="remove_watchlist"),
    path("close_listing/<int:list_id>", views.close_listing, name="close_listing"),
    path("comments/<int:list_id>", views.comments, name="comments"),
    path("watchlist", views.user_watchlist, name="user_watchlist")
]
