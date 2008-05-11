from django.test import TestCase
from django.test.client import Client
from django.db import IntegrityError
from django.contrib.auth.models import User

from tod.game.models import Game
from tod.player.models import Player

class PlayerTest(TestCase):
    """Tests the creation of a player object with blank, minimal, and maximal inputs
    """
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
        """Tests the creation of a player object with no input
        """
        datum = self.data[0]
        player = Player(**datum)
        self.assertRaises(IntegrityError, player.save) 

    def test_create_minimal(self):
        """Tests the creation of a player object with minimal input
        """
        datum = self.data[1]
        player = Player(**datum)
        player.game = self.test_game
        player.save()
        self.failUnlessEqual(player.name, datum['name'])

    def test_create_maximal(self):
        """Tests the creation of a player object with maximal input
        """
        datum = self.data[2]
        player = Player(**datum)
        player.game = self.test_game
        player.save()
        self.failUnlessEqual(player.name, datum['name'])
        self.failUnlessEqual(player.score, datum['score'])

class PlayerScoreTest(TestCase):
    """Tests score functionality
    """
    fixtures = ["pair"]
    def test_update_score(self):
        """Tests that the update_score function changes the player's score
        """
        player = Player.objects.get(name="Alice")
        self.failUnlessEqual(player.score, 0)
        player.update_score(score=1)
        self.failUnlessEqual(player.score, 1)


class PlayerViewTest(TestCase):
    """Tests the player create url for an authenticated user
    """
    fixtures = ["all_difficulties"]
    def setUp(self):
        self.client = Client()
        self.client.login(username="laura", password="laura")
        self.game = Game.objects.get(name="TestGame")
        create = '/player/%d/create/' % (self.game.id)
        self.urls = {
            create: 302,
            }

    def test_noPlayers(self):
        """Tests that it redirects to the player create page if there are no players
        """
        response = self.client.get('/player/1/')        
        self.assertRedirects(response, "/player/1/create/")

    def test_playerList(self):
        """Tests that the player list displays player objects
        """
        player = Player.objects.create(name="Alice", game=Game.objects.get(name="TestGame"))
        response = self.client.get('/player/1/')
        self.assertContains(response, "Alice")

    def test_playerCreate(self):
        """Tests that a post creates a player
        """
        response = self.client.post('/player/1/create/', {"name": "Ed"})
        self.failUnlessEqual(Player.objects.count(), 1)

    def test_playerForm(self):
        """Tests that a get returns the player form
        """
        response = self.client.get('/player/1/create/')
        self.assertContains(response, "create_player")

    def test_playerDelete(self):
        """Tests that the delete view deletes a player object
        """
        player = Player.objects.create(name="Frank", game = Game.objects.get(name="TestGame"))
        response = self.client.post('/player/1/delete/')
        self.failUnlessEqual(Player.objects.count(), 0)

class UnauthenticatedPlayerViewTest(TestCase):
    """Tests the player create url for an unauthenticated user
    """
    fixtures = ["all_difficulties"]
    def setUp(self):
        self.client = Client()
        self.game = Game.objects.get(name="TestGame")
        create = '/player/%d/create/' % (self.game.id)
    
    def test_unauthenticated(self):
        """Tests the player create url for an unauthenticated user
        """
        url = '/player/%d/create/' % (self.game.id)
        response = self.client.get(url)
        self.assertRedirects(response, 'http://testserver/accounts/login/?next='+url, status_code=302, target_status_code=200)
