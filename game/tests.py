from django.test import TestCase
from django.test.client import Client
from django.db import IntegrityError
from django.contrib.auth.models import User
from tod.prompt.models import Prompt
from tod.game.models import Game

class GameTest(TestCase):
    def setUp(self):
        (self.laura, created) = User.objects.get_or_create(username="Laura")
        self.data = [
            {},
            {
                'name': 'TestGame',
                'status': 'completed',
                'user': self.laura,
            },
            {
                'name': 'TestGame',
                'status': 'completed',
                'user': self.laura,
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
        self.failUnlessEqual(game.name, 'TestGame')
        self.failUnlessEqual(game.status, 'completed')
        self.failUnlessEqual(game.user, self.laura)

    def test_create_maximal(self):
        datum = self.data[2]
        game = Game(**datum)
        self.failUnlessEqual(game.max_difficulty, 7)

class GameViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.laura = User.objects.create_user(username="Laura", password="laura", email="laura.m.madsen@gmail.com")
        self.game = Game.objects.create(name="Test Game", status="created", user=self.laura)
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

class MaxDifficultyTest(TestCase):
    """ test that max difficulty properly restricts prompts, also test that other user's private prompts are not included
    """
    #create ten prompts, one for each difficulty level, plus 3 extra at 1,5 and 10 belonging to the current user, and 3 at 1, 5 and 10 belonging to another user
    #create a game with no max difficulty
    #create a game with a max difficulty of 7
    fixtures = ["all_difficulties"]
    def setUp(self):
        pass
    def test_max_difficulty_blank(self):
    #test that the prompt count equals the total number of prompts excluding those private to the other user if no max difficulty is set
    #test that the prompt count for the game is thirteen
        self.game = Game.objects.get(name='TestGame')
        prompts = self.game.availablePrompts()
        self.failUnlessEqual(Prompt.objects.count(), 16)
        self.failUnlessEqual(prompts.count(), 13)
    def test_max_difficulty(self):
    #test that the prompt count when the max difficulty is set is equal to the number of prompts at or below max difficulty
    #test that the prompt count is nine
        self.game = Game.objects.get(name='WimpyGame')
        prompts = self.game.availablePrompts()
        self.failUnlessEqual(prompts.count(), 9)
    #test that all prompts included in the prompt count when the max difficulty is set are at or under the max difficulty
    #get the list of prompts available for the game
    #loop through the prompts and assert that their difficulty is at or below 7

class TaggedItemTest(TestCase):
    """test that prompts with tags selected for the game are excluded from the available prompts"""
    #create a fixture with ten prompts, one tagged for nudity and one tagged as mature content
    #create a game with tags for nudity and adult
    #test that the available prompts for the game is 8
    fixtures = ["tagged_items"]
    def setUp(self):
        pass
    def test_tagged_item(self):
        self.game = Game.objects.get(name="TagsGame")
        prompts = self.game.availablePrompts()
        self.failUnlessEqual(Prompt.objects.count(), 10)
        self.failUnlessEqual(prompts.count(), 8)