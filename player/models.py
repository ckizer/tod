from django.db import models

from tod.game.models import Game

class Player(models.Model):
    """Provides functionality for the player object
    """
    name = models.CharField(max_length=20)
    game = models.ForeignKey(Game, related_name="players", blank=True)
    score = models.IntegerField(default=0, null=False, blank=True)
    
    def __unicode__(self):
        return self.name

    def update_score(self, score):
        """Updates the score for the player
        """
        self.score = self.score + score
        self.save()
