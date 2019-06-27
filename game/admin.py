from django.contrib import admin
from game.models import Game, Label
# Register your models here.


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'uuid']


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'uuid']
