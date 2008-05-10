from django.test import TestCase
from django.test.client import Client
from django.db import IntegrityError
from django.contrib.auth.models import User
from tod.prompt.models import Prompt
from tod.game.models import Game
from tod.game.forms import GameForm

GAME_DATA = [
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



class GameTest(TestCase):
    """Test elements of the Game model
    """
    def setUp(self):
        (self.laura, created) = User.objects.get_or_create(username="Laura")

    def test_create_blank(self):
        """Test game creation with no data
        """
        datum = GAME_DATA[0]
        game = Game(**datum)
        self.assertRaises(IntegrityError, game.save) 

    def test_create_minimal(self):
        """Test game creation with the least possible data
        """
        datum = GAME_DATA[1]
        game = Game(**datum)
        self.failUnlessEqual(game.name, 'TestGame')
        self.failUnlessEqual(game.status, 'completed')
        self.failUnlessEqual(game.user, self.laura)

    def test_create_maximal(self):
        """Test game creation with all possible data
        """
        datum = GAME_DATA[2]
        game = Game(**datum)
        self.failUnlessEqual(game.max_difficulty, 7)

class GameStatusTest(TestCase):
    """Test that an existing game proceeds normally through statuses

    Provide a fixture that has:
    A newly created game
    A valid user
    Several prompts to assign
    """
    fixtures = ['game_status']
    def setUp(self):
        self.user = User.objects.get(username="laura")
        self.game = Game.objects.get()

    def test_status(self):
        self.failUnlessEqual(self.game.status, 'created')
        #Add 2 players and mark the game players_added
        for player in ['alice', 'bob']:
            Player.objects.create(name=name, game=self.game)
        self.game.players_added()
        self.failUnlessEqual(self.game.status, 'players_added')
        #assign prompts
        self.game.assign_prompts(self.game.availablePrompts())
        self.failUnlessEqual(self.game.status, 'prompts_selected')
        #start game
        self.game.in_progress()
        self.failUnlessEqual(self.game.status, 'in_progress')
        #complete game
        while self.game.current_prompt():
            prompt = self.game.current_prompt()
            prompt.complete()
        self.failUnlessEqual(self.game.status, 'completed')
        

class GameFormTest(TestCase):
    """Test creation the Game model via form
    """
    fixtures = ["user"]
    def setUp(self):
        self.user = User.objects.get(username="laura")

    def submit_form(self, datum):
        form = GameForm(self.user, datum)
        if form.is_valid():
            game = form.save(commit=False)
        return game

    def test_create_blank(self):
        """Test game creation with no data
        """
        game = self.submit_form(GAME_DATA[0])
        self.assertRaises(IntegrityError, game.save) 

    def test_create_minimal(self):
        """Test game creation with the least possible data
        """
        game = self.submit_form(GAME_DATA[1])
        game.save()
        self.failUnlessEqual(game.name, 'TestGame')
        self.failUnlessEqual(game.status, 'completed')
        self.failUnlessEqual(game.user, self.user)

    def test_create_maximal(self):
        """Test game creation with all possible data
        """
        game = self.submit_form(GAME_DATA[2])
        game.save()
        self.failUnlessEqual(game.max_difficulty, 7)
        self.failUnlessEqual(game.tags.count(), 3)

class GameViewTest(TestCase):
    def setUp(self):
        """Test game creation through the views with all possible data
        """
        self.client = Client()
        self.laura = User.objects.create_user(username="Laura", password="laura", email="laura.m.madsen@gmail.com")
        self.game = Game.objects.create(name="Test Game", status="created", user=self.laura)
        absolute_url = '/game/%d/' % (self.game.id)
        self.urls = {
            '/game/': 200,
            absolute_url: 302,
            }
    
    def test_unauthenticated(self):
        """Test trying to view the game while not authenticated
        """
        for url, status_code in self.urls.items():
            response = self.client.get(url)
            self.assertRedirects(response, 'http://testserver/accounts/login/?next='+url, status_code=302, target_status_code=200)

    def test_authenticated(self):
        """Test trying to view the game while authenticated
        """
        self.client.login(username="Laura", password="laura")
        for url, status_code in self.urls.items():
            response = self.client.get(url)
            self.failUnlessEqual(response.status_code, status_code)    

class MaxDifficultyTest(TestCase):
    """ test that max difficulty properly restricts prompts, also test that other user's private prompts are not included

    Provide a fixture with 16 prompts
    10 public (1 for each difficulty)
    3 private to our user
    3 private to another user

    Provide a fixture with 2 games
    One with no max difficulty
    One with a max difficulty of 7
    """
    fixtures = ["all_difficulties"]
    def setUp(self):
        pass
    def test_max_difficulty_blank(self):
        """Test that all prompts are available if max difficulty is not set

        """
        self.game = Game.objects.get(name='TestGame')
        prompts = self.game.availablePrompts()
        self.failUnlessEqual(Prompt.objects.count(), 16)
        #test that the prompt count equals the total number of prompts 
        #excluding those private to the other users
        #With 3 prompts private to the other user the prompt count for the game is thirteen
        self.failUnlessEqual(prompts.count(), 13)

    def test_max_difficulty(self):
        """Test that only sub-max prompts are displayed if a max difficulty is set
        """
        self.game = Game.objects.get(name='WimpyGame')
        prompts = self.game.availablePrompts()
        #test that the prompt count is 9
        self.failUnlessEqual(prompts.count(), 9)
        #TODO - loop through the prompts and assert that their difficulty is at or below 7

class TaggedItemTest(TestCase):
    """test that prompts with tags selected for the game are excluded from the available prompts
    create a fixture 
    ten prompts (1 tagged for nudity and 1 tagged as mature content)
    A game with tags for nudity and adult
    """
    fixtures = ["tagged_items"]
    def setUp(self):
        pass
    def test_tagged_item(self):
        self.game = Game.objects.get(name="TagsGame")
        prompts = self.game.availablePrompts()
        self.failUnlessEqual(Prompt.objects.count(), 10)
        #test that the available prompts for the game is 8
        self.failUnlessEqual(prompts.count(), 8)
