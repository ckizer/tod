from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=50)
    game = models.ForeignKey('Game')
    score = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return self.name
