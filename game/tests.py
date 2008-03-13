from django.test import TestCase
from django.test.client import Client
from django.db import IntegrityError
from django.contrib.auth.models import User

from tod.game.models import Game

class GameTest(TestCase):
    def setUp(self):
        (laura, created) = User.objects.get_or_create(username="Laura")
        self.data = [
            {},
            {
                'name': 'TestGame',
                'status': 'completed',
                'user': laura,
            },
            {
                'name': 'TestGame',
                'status': 'completed',
                'user': laura,
                'max_difficulty': 7,
            },
            ]

    def test_create_blank(self):
        datum = self.data[0]
        game = Game(**datum)
        self.assertRaises(IntegrityError, game.save) 

    def test_create_minimal(self):
        datum = self.data[1]
        game = Game(**datum)

    def test_create_maximal(self):
        datum = self.data[2]
        game = Game(**datum)

class GameViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        laura = User.objects.create_user(username="Laura", password="laura", email="laura.m.madsen@gmail.com")
        self.game = Game.objects.create(name="Test Game", status="created", user=laura)
        absolute_url = '/game/%d/' % (self.game.id)
        self.urls = {
            '/game/': 200,
            absolute_url: 302,
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
