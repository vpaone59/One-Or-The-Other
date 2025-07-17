from django.contrib import admin

# Register your models here.
from .models.choice import Choice
from .models.game import Game
from .models.user_choice import UserChoice

admin.site.register(Choice)
admin.site.register(Game)
admin.site.register(UserChoice)
