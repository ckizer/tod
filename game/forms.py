from django.forms import ModelForm, Form
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
        
class RoundForm(forms.Form):
    """ Provides the form for selecting the number of rounds
    """
    rounds = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.game = kwargs.pop('game') if kwargs.has_key('game') else None
        super(RoundForm, self).__init__(*args, **kwargs)

    def clean_rounds(self):
        data = self.cleaned_data['rounds']
        if not data.isdigit():
            raise forms.ValidationError("Please select a number between 1 and the maximum rounds available")
        if not (1 <= int(data) <= self.game.maximumRounds()):
            raise forms.ValidationError("Please select a number between 1 and the maximum number of rounds available.")
        return data

    def save(self):
        return int(self.cleaned_data['rounds'])

