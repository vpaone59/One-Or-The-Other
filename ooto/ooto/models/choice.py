from django.db import models


class Choice(models.Model):
    """Choice model."""

    description = models.CharField(max_length=255, unique=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description}"
