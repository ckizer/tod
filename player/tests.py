from django.test import TestCase
from django.test.client import Client
from django.db import IntegrityError
from django.contrib.auth.models import User

from tod.game.models import Game
from tod.player.models import Player

class PlayerTest(TestCase):
    def setUp(self):
        (laura, created) = User.objects.get_or_create(username="Laura")        
        (self.test_game, created) = Game.objects.get_or_create(name="Test_Game", user=laura)
        self.data = [
            {},
            {
                'name': 'Peter',
            },
            {
                'name': 'Peter',
                'score': 0,
            },
            ]

    def test_create_blank(self):
        datum = self.data[0]
        player = Player(**datum)
        self.assertRaises(IntegrityError, player.save) 

    def test_create_minimal(self):
        datum = self.data[1]
        player = Player(**datum)
        player.game = self.test_game
        player.save()
        self.failUnlessEqual(player.name, datum['name'])

    def test_create_maximal(self):
        datum = self.data[2]
        player = Player(**datum)
        player.game = self.test_game
        player.save()
        self.failUnlessEqual(player.name, datum['name'])
        self.failUnlessEqual(player.score, datum['score'])
