from django.urls import path
from .views import (
    home_view,
    cast_vote,
    history_view,
    game_view,
    admin_view,
    admin_add_choice,
    admin_add_game,
    admin_delete_choice,
    admin_undo_delete_choice,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("vote/<int:game_id>/<int:choice_id>/", cast_vote, name="vote"),
    path("history/", history_view, name="history"),
    path("history/game/<int:game_id>/", game_view, name="game"),
    path("admin/", admin_view, name="admin"),
    path("admin/add-choice/", admin_add_choice, name="admin_add_choice"),
    path("admin/add-game/", admin_add_game, name="admin_add_game"),
    path(
        "admin/delete-choice/<int:choice_id>/",
        admin_delete_choice,
        name="admin_delete_choice",
    ),
    path(
        "admin/undo-delete-choice/<int:choice_id>/",
        admin_undo_delete_choice,
        name="admin_undo_delete_choice",
    ),
]
