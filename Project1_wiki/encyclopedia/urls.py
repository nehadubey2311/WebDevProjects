from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:pageTitle>", views.wikiPage, name="wikipages"),
    path("addpage", views.addPage, name="addPage"),
    path("search", views.search, name="search")
]
