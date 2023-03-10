from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),

    path("new", views.new, name="new"),

    path("<str:title>", views.get, name="get"),
    path("<str:title>/edit", views.edit, name="edit"),
]
