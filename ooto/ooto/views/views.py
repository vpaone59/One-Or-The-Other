import logging
from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from ooto.models import Choice, Game, UserChoice

logger = logging.getLogger(__name__)


def home_view(request):
    """Render the home page with today's games."""
    try:
        games = Game.objects.filter(game_date=date.today())
        return render(request, "ooto/home.html", {"games": games})
    except Exception as e:
        logger.error("Error rendering home page: %s", e)
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
        logger.error("Error processing vote: %s", e)
        return HttpResponseServerError("Internal Server Error")


def history_view(request):
    """Render the history page with all games."""
    try:
        all_games = Game.objects.all()
        return render(request, "ooto/history.html", {"all_games": all_games})
    except Exception as e:
        logger.error("Error rendering history page: %s", e)
        return HttpResponseServerError("Internal Server Error")


def game_view(request, game_id):
    """Render the game page with the game details."""
    try:
        game = Game.objects.get(id=game_id)
        user_choices = UserChoice.objects.filter(game_id=game).order_by(
            "-datetime_created"
        )
        return render(
            request,
            "ooto/game.html",
            {
                "game": game,
                "user_choices": user_choices,
            },
        )
    except Exception as e:
        logger.error("Error rendering game page: %s", e)
        return HttpResponseServerError("Internal Server Error")


# @login_required
def admin_view(request):
    """Render the admin page."""
    try:
        choices = Choice.objects.all().order_by("-datetime_created")
        games = Game.objects.all().order_by("-game_date")

        # Get recently deleted choice from session if exists
        recently_deleted_choice = None
        if "recently_deleted_choice" in request.session:
            choice_data = request.session["recently_deleted_choice"]
            recently_deleted_choice = {
                "id": choice_data.get("id"),
                "description": choice_data.get("description"),
            }

        return render(
            request,
            "ooto/admin.html",
            {
                "choices": choices,
                "games": games,
                "recently_deleted_choice": recently_deleted_choice,
            },
        )
    except Exception as e:
        logger.error("Error rendering admin page: %s", e)
        return HttpResponseServerError("Internal Server Error")


# @login_required
def admin_add_choice(request):
    """Add a new choice."""
    if request.method == "POST":
        try:
            description = request.POST.get("description")
            if description:
                Choice.objects.create(description=description)
            return redirect("admin")
        except Exception as e:
            logger.error("Error adding choice: %s", e)
            return HttpResponseServerError("Internal Server Error")
    return redirect("admin")


# @login_required
def admin_add_game(request):
    """Add a new game."""
    if request.method == "POST":
        try:
            first_choice_id = request.POST.get("first_choice")
            second_choice_id = request.POST.get("second_choice")
            game_date = request.POST.get("game_date")

            if first_choice_id and second_choice_id and game_date:
                first_choice = Choice.objects.get(id=first_choice_id)
                second_choice = Choice.objects.get(id=second_choice_id)

                if first_choice_id != second_choice_id:
                    Game.objects.create(
                        first_choice=first_choice,
                        second_choice=second_choice,
                        game_date=game_date,
                    )
            return redirect("admin")
        except Exception as e:
            logger.error("Error adding game: %s", e)
            return HttpResponseServerError("Internal Server Error")
    return redirect("admin")


# @login_required
def admin_delete_choice(request, choice_id):
    """Delete a choice."""
    if request.method == "POST":
        try:
            choice = Choice.objects.get(id=choice_id)

            # Store choice data in session for potential undo
            request.session["recently_deleted_choice"] = {
                "id": choice.id,
                "description": choice.description,
            }

            # Save the choice data to the session and delete the choice
            choice.delete()

            return redirect("admin")
        except Exception as e:
            logger.error("Error deleting choice: %s", e)
            return HttpResponseServerError("Internal Server Error")
    return redirect("admin")


# @login_required
def admin_undo_delete_choice(request, choice_id):
    """Undo a choice deletion."""
    try:
        if "recently_deleted_choice" in request.session:
            choice_data = request.session["recently_deleted_choice"]

            # Recreate the choice
            Choice.objects.create(description=choice_data.get("description"))

            # Clear the deleted choice from session
            del request.session["recently_deleted_choice"]

        return redirect("admin")
    except Exception as e:
        logger.error("Error undoing choice deletion: %s", e)
        return HttpResponseServerError("Internal Server Error")
