#!/usr/bin/python
import sys
import os
from os.path import dirname
sys.path.insert(0, dirname(os.getcwd()))
os.environ['DJANGO_SETTINGS_MODULE'] = 'tod.settings'

from tod.game.models import Game, Player

#[g.delete() for g in Game.objects.all()]
for name in ["New Years", "Birthday", "4th of July", "International Peter Day"]:
    (g, created)=Game.objects.get_or_create(name=name)

print "games:", Game.objects.all()

g=Game.objects.get(name="New Years")

for player in ["Peter", "Chrissy", "Briana", "Caitlin", "Laura"]:
    (p, created)=Player.objects.get_or_create(name=player, game=g)

print "players:", g.player_set.all()
