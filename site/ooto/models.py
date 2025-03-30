from django.db import models


class Choice(models.Model):
    """Choice model."""

    description = models.CharField(max_length=255, unique=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description}"


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


class UserChoice(models.Model):
    """UserChoice model."""

    user = models.CharField(max_length=255)
    user_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    anonymous_name = models.CharField(max_length=255)
    remote_address = models.CharField(max_length=255)
    datetime_created = models.DateTimeField(auto_now_add=True)
