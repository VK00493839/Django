from django.urls import path
from . import views


urlpatterns = [
    path('', views.teams, name='teams'),
    path('players/<int:id>/', views.players, name='players'),

    path('<int:id>/details/', views.playerHistory_details,
         name="playerHistory_details"),
    path('<int:id>/edit/', views.playerHistory_edit, name="playerHistory_edit"),

    path('matchesList/', views.matchesList, name='matches_list'),
    path('add/', views.matchesAdd, name="matches_add"),

    path('points/', views.pointsView, name='points'),
]
