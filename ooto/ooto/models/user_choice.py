from django.db import models
from .choice import Choice
from .game import Game


class UserChoice(models.Model):
    """UserChoice model."""

    user = models.CharField(max_length=255)
    user_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    anonymous_name = models.CharField(max_length=255)
    remote_address = models.CharField(max_length=255)
    datetime_created = models.DateTimeField(auto_now_add=True)
