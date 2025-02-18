from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tasks", views.tasks, name="tasks"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("enter", views.enter, name="enter"),
    path("logout", views.logout, name="logout"),
]
