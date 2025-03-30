import logging
from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from .models.choice import Choice
from .models.game import Game
from .models.user_choice import UserChoice

logger = logging.getLogger(__name__)


def home_view(request):
    """Render the home page with today's games."""
    try:
        games = Game.objects.filter(game_date=date.today())
        return render(request, "ooto/home.html", {"games": games})
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        return HttpResponseServerError("Internal Server Error")


def cast_vote(request, game_id, choice_id):
    """Process a vote."""
    try:
        choice = Choice.objects.get(id=choice_id)
        game = Game.objects.get(id=game_id)
        if request.user.is_authenticated:
            UserChoice.objects.create(
                user=request.user.username, user_choice=choice, game_id=game
            )
        else:
            remote_address = request.META.get("REMOTE_ADDR")
            UserChoice.objects.create(
                user="Anonymous",
                remote_address=remote_address,
                user_choice=choice,
                game_id=game,
            )
        return redirect("history")
    except Exception as e:
        logger.error(f"Error processing vote: {e}")
        return HttpResponseServerError("Internal Server Error")


def history_view(request):
    """Render the history page with all games."""
    try:
        all_games = Game.objects.all()
        return render(request, "ooto/history.html", {"all_games": all_games})
    except Exception as e:
        logger.error(f"Error rendering history page: {e}")
        return HttpResponseServerError("Internal Server Error")


def game_view(request, game_id):
    """Render the game page with the game details."""
    try:
        game = Game.objects.get(id=game_id)
        return render(request, "ooto/game.html", {"game": game})
    except Exception as e:
        logger.error(f"Error rendering game page: {e}")
        return HttpResponseServerError("Internal Server Error")
