from django.db import models
from .choice import Choice


class Game(models.Model):
    """Game model."""

    first_choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, related_name="first_choice"
    )
    second_choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, related_name="second_choice"
    )
    game_date = models.DateField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_choice} or {self.second_choice}"
