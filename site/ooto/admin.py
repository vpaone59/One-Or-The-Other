from django.contrib import admin

# Register your models here.
from .models import Choice, Game, UserChoice

admin.site.register(Choice)
admin.site.register(Game)
admin.site.register(UserChoice)
