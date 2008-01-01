from django.db import models

class Game(models.Model):
    name = models.Charfield(max_length=50)


class Player(models.Model):
    name = models.Charfield(max_length=50)
    game = models.ForeignKey('Game')
    score = models.IntegerField()
