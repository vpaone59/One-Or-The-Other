from django.urls import path
from .views import home_view, cast_vote, history_view, game_view

urlpatterns = [
    path("", home_view, name="home"),
    path("vote/<int:game_id>/<int:choice_id>/", cast_vote, name="vote"),
    path("history/", history_view, name="history"),
    path("game/<int:game_id>/", game_view, name="game"),
]
