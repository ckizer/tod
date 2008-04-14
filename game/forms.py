from django.newforms import ModelForm
from django import newforms as forms
from tod.game.models import Game

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'max_difficulty')
