from django.db import models

from tod.game.models import Game

class Player(models.Model):
    name = models.CharField(max_length=50)
    game = models.ForeignKey(Game, blank=True)
    score = models.IntegerField(default=0, null=False, blank=True)
    
    def __str__(self):
        return self.name

    def update_score(self, score):
        self.score = self.score + score
        self.save()
