from django.newforms import ModelForm
from django import newforms as forms

from tod.player.models import Player

class PlayerForm(ModelForm):
    """Provides a form for creating a player
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') if kwargs.has_key('user') else None
        super(PlayerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Player
        fields = ('name')

    def save(self, commit=True):
        player = super(PlayerForm, self).save(commit=False)
        if commit:
            player.save()
        return player
