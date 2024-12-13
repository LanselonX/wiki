from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_func, name="entry"),
    path("search/", views.search_func, name="search"),
]
