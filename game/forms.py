from django.forms import ModelForm
from django import forms

from tod.game.models import Game

class GameForm(ModelForm):
    """Provides a form for creating a game

    TODO - (defer) test that the form properly creates a game object with specified tagged items
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') if kwargs.has_key('user') else None
        super(GameForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Game
        fields = ('name', 'max_difficulty')

    def clean_max_difficulty(self):
        data = self.cleaned_data['max_difficulty']
        if not (1 <= data <= 10):
            raise forms.ValidationError('Max Difficulty must be between 1 and 10.')
        return data

    def save(self, commit=True):
        game = super(GameForm, self).save(commit=False)
        game.user = self.user
        if commit:
            game.save()
        return game
        
