from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("create", views.create_entry, name="create"),
    path("redirect", views.find_entry, name="redirect"),
    path("random", views.random_entry, name="random"),
    path("edit/<str:title>/", views.edit_entry, name="edit")
]
