from django.newforms import ModelForm
from django import newforms as forms

from tod.game.models import Game

class GameForm(ModelForm):
    """Provides a form for creating a game

    TODO - test that the form properly creates a game object with specified tagged items
    """
    class Meta:
        model = Game
        fields = ('name', 'max_difficulty')
