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

class PlayerViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        laura = User.objects.create_user(username="Laura", password="laura", email="laura.m.madsen@gmail.com")
        self.game = Game.objects.create(name="Test Game", status="created", user=laura)
        self.player = Player.objects.create(name="Peter", game=self.game)
        create = '/player/%d/create' % (self.game.id)
        self.urls = {
            '/player/%d/create/': 302,
            }
    
    def test_unauthenticated(self):
        for url, status_code in self.urls.items():
            response = self.client.get(url)
            self.assertRedirects(response, 'http://testserver/accounts/login/?next='+url, status_code=302, target_status_code=200)

    def test_authenticated(self):
        self.client.login(username="Laura", password="laura")
        for url, status_code in self.urls.items():
            response = self.client.get(url)
            self.failUnlessEqual(response.status_code, status_code)
