from django.newforms import ModelForm
from django import newforms as forms

from tod.game.models import Game

class GameForm(ModelForm):
    """Provides a form for creating a game

    TODO - test that the form properly creates a game object with specified tagged items
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') if kwargs.has_key('user') else None
        super(GameForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Game
        fields = ('name', 'max_difficulty')

    def save(self, commit=True):
        game = super(GameForm, self).save(commit=False)
        game.user = self.user
        if commit:
            game.save()
        return game
        
