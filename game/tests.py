from BeautifulSoup import BeautifulSoup

from django.test import TestCase
from django.test.client import Client
from django.db import IntegrityError
from django.contrib.auth.models import User
from tod.prompt.models import Prompt, TaggedItem
from tod.player.models import Player
from tod.game.models import Game
from tod.game.forms import GameForm

GAME_DATA = [
    {},
    {
        'name': 'TestGame',
        'status': 'completed',
        },
    {
        'name': 'TestGame',
        'status': 'completed',
        'max_difficulty': 7,
        },
    ]



class GameTest(TestCase):
    """Test elements of the Game model
    """
    def setUp(self):
        (self.laura, created) = User.objects.get_or_create(username="laura")

    def test_create_blank(self):
        """Test game creation with no data
        """
        datum = GAME_DATA[0]
        game = Game(**datum)
        self.assertRaises(IntegrityError, game.save) 

    def test_createMinimal(self):
        """Test game creation with the least possible data
        """
        datum = GAME_DATA[1]
        datum['user'] = self.laura
        game = Game(**datum)
        game.save()
        self.failUnlessEqual(game.name, 'TestGame')
        self.failUnlessEqual(game.status, 'completed')
        self.failUnlessEqual(game.user, self.laura)
        self.failUnlessEqual(game.get_absolute_url(), '/game/%d/' % game.id)

    def test_createMaximal(self):
        """Test game creation with all possible data
        """
        datum = GAME_DATA[2]
        datum['user'] = self.laura
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
            Player.objects.create(name=player, game=self.game)
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
        
class GamePromptTest(TestCase):
    """Test that the Game Prompts are assigned to the game
    """
    fixtures = ["pair", "all_difficulties"]
    def setUp(self):
        self.game = Game.objects.get(name="TestGame")
        self.prompts = Prompt.objects.all()[:3]
        self.game.assign_prompts(self.prompts)
        
    def test_assignPrompts(self):
        """test that assign_prompt saves the prompts assigned to a game
        """
        self.failUnlessEqual(self.game.gameprompt_set.count(), self.prompts.count())
        #test that as we complete prompts they fall out of circulation
        prompts_remaining = len(self.prompts)
        while self.game.current_prompt():
            #the prompt count is the count of prompts that are not complete
            prompt_count = self.game.gameprompt_set.filter(is_complete=False).count()
            self.failUnlessEqual(prompt_count, prompts_remaining)
            current_prompt = self.game.current_prompt()
            #complete the prompt to take it out of circulation
            current_prompt.complete()
            #there should not be one less prompt remaining because it's complete
            prompts_remaining -= 1

    def test_idempotentCurrentPrompt(self):
        """Test that, if no action happens, current_prompt always returns the same prompt
        """
        current_prompt = self.game.current_prompt()
        still_current_prompt = self.game.current_prompt()
        self.failUnlessEqual(current_prompt, still_current_prompt)

    def test_completeScore(self):
        """Test that when we complete a prompt the difficulty is added to the score
        """
        player = self.game.players.all()[0] 
        score = player.score
        additional_score = self.game.current_prompt().prompt.difficulty
        self.game.resolve_current_prompt()
        player = Player.objects.get(id=1)
        self.failUnlessEqual(player.score, additional_score + score)

    def test_wimpOut(self):
        """Test that when we wimp out the score doesn't change
        """
        player = self.game.players.all()[0] 
        score = player.score
        self.game.resolve_current_prompt("wimp out")
        player = Player.objects.get(id=1)
        self.failUnlessEqual(player.score, score)

    def test_incrementPlayer(self):
        """Test that when prompts are completed, the current player is incremented by one
        """
        player = self.game.players.all()[0]
        current_prompt = self.game.current_prompt()
        self.game.resolve_current_prompt()
        self.failUnlessEqual(self.game.current_player(), self.game.players.all()[1])

    def test_completeGamePrompt(self):
        """Test that completing the current prompt changes its is_complete from False to True
        """
        current_prompt = self.game.current_prompt()
        self.failUnlessEqual(current_prompt.is_complete, False)
        current_prompt.complete()
        self.failUnlessEqual(current_prompt.is_complete, True)
        
class GameFormTest(TestCase):
    """Test creation the Game model via form
    """
    fixtures = ["user"]
    def setUp(self):
        self.user = User.objects.get(username="laura")

    def submit_form(self, datum):
        form = GameForm(user=self.user, data=datum)
        if form.is_valid():
            game = form.save()
        return game

    def test_create_blank(self):
        """Test game creation with no data
        """
        form = GameForm(user=self.user, data=GAME_DATA[0])
        form.is_valid()
        self.assertRaises(ValueError, form.save) 

    def test_create_minimal(self):
        """Test game creation with the least possible data
        """
        game = self.submit_form(GAME_DATA[1])
        self.failUnlessEqual(game.name, 'TestGame')
        self.failUnlessEqual(game.status, 'created')
        self.failUnlessEqual(game.user, self.user)

    def test_create_maximal(self):
        """Test game creation with all possible data
        """
        game = self.submit_form(GAME_DATA[2])
        for name in ['one', 'two', 'three']:
            game.tags.create(tag=name)
        self.failUnlessEqual(game.max_difficulty, 7)
        self.failUnlessEqual(game.tags.count(), 3)

class RoundsAvailableTest(TestCase):
    fixtures = ["beginning_prompts", "user"]
    def setUp(self):
        laura = User.objects.get(username="laura")
        self.game = Game.objects.create(name="TestGame", user=laura)
    def test_maximumRounds(self):
        """Tests that the number of rounds listed as available on the select_rounds page is accurate
        """
        Player.objects.create(name='Alice', game=self.game)
        self.failUnlessEqual(self.game.availablePrompts().count(), 40)
        self.failUnlessEqual(self.game.maximumRounds(), 40)

class MaximumRoundsTest(TestCase):
    fixtures = ["maximum_rounds"]
    def setUp(self):
        self.game = Game.objects.get(name="TestGame")
    def test_maximumRounds(self):
        """Comprehensively tests combinations of player count and rounds
        in difficulty levels to make sure rounds available returns a reasonable number
        """
        # confirm that game has 1 player and 15 prompts, {'1': 5, '2': 4, '3':3, '4': 2, '5': 1}
        test_tuple = [(1, 5), (2, 4), (3, 3), (4, 2), (5, 1), (6,0), (7,0), (8,0), (9,0), (10, 0)]
        existing_prompts = [(difficulty+1, len(prompts)) for difficulty, prompts in enumerate(self.game.segmentedPrompts())]
        self.failUnlessEqual(test_tuple, existing_prompts)
        
        # assert that with player count of 1 through 6, we get 15, 6, 3, 2, 1, 0 respectively
        test_maximum_rounds = [15, 6, 3, 2, 1, 0]
        for i in range(6):
            Player.objects.create(name='player_%d' % (i + 1), game=self.game)
            self.failUnlessEqual(self.game.maximumRounds(), test_maximum_rounds[i])



class GameCreateTest(TestCase):
    """Test that a created game with prompts available assigns the selected number of rounds
    
    Test that the rounds assigned have prompts with all equal difficulties
    Test that the rounds are all filled if there are sufficient prompts
    Test that not all rounds are assigned if there aren't enough prompts

    Create a fixture with:
    one game
    several prompts
    assign one player to test with sufficient prompts and two players to test insufficient prompts
    """
    fixtures = ["all_difficulties"]
    def setUp(self):
        self.game = Game.objects.get(name="TestGame")

    def test_excessPrompts(self):
        """Tests that rounds selected equals rounds created with sufficient prompts
        """
        Player.objects.create(name='Alice', game=self.game)
        self.game.players_added()
        self.game.create_game(rounds_selected = 5)
        rounds_assigned = self.game.gameprompt_set.count()
        self.failUnlessEqual(rounds_assigned, 5)

    def test_insufficientPrompts(self):
        """Tests that rounds selected equals maximum rounds available with insufficient prompts

        Tests that all prompts in a round have equal difficulty
        """
        for player in ['alice', 'bob']:
            Player.objects.create(name=player, game=self.game)
        self.game.players_added()
        self.game.create_game(rounds_selected = 5)
        rounds_assigned = self.game.gameprompt_set.count()/self.game.players.count()
        self.failUnlessEqual(rounds_assigned, 3)
        difficulty = None
        while self.game.current_prompt():
            for player in self.game.players.all():
                current_prompt = self.game.current_prompt()
                if not difficulty:
                    difficulty = current_prompt.prompt.difficulty
                else:
                    self.failUnlessEqual(difficulty, current_prompt.prompt.difficulty)
                current_prompt.complete()
            difficulty = None

class AvailableSegmentedPromptsTestCase(TestCase):
    """ walk through different prompt hierarchy scenarios and make sure 
        the right number of prompts get assinged
    """
    def setUp(self):
        user = User.objects.create_user("peter", "peter@emlprime.com", "test")
        self.game = Game.objects.create(name="TestGame", user=user)
        player_names = ['alice', 'bob']
        for player in player_names:
            Player.objects.create(name=player, game=self.game)
        self.player_count = len(player_names)

    def test_noPrompts(self):
        self.assertEqual(self.game.available_segmented_prompts([], self.player_count), False)
    
    def test_enoughPrompts(self):
        self.assertEqual(self.game.available_segmented_prompts([range(self.player_count)], self.player_count), False)
    
class CurrentRoundTestCase(TestCase):
    """ Find out the current round
    """
    def setUp(self):
        user = User.objects.create_user("peter", "peter@emlprime.com", "test")
        self.game = Game.objects.create(name="TestGame", user=user)
        player_names = ['alice', 'bob']
        for player in player_names:
            Player.objects.create(name=player, game=self.game)
        self.player_count = len(player_names)
        game_prompts = [Prompt.objects.create(name="foo_%d" % i, difficulty=1, owner=user) for i in range(10)]
        self.game.assign_prompts(game_prompts)

    def test_firstRound(self):
        self.assertEqual(self.game.current_round(), 1)

    def test_halfwayThroughFirstRound(self):
        self.game.resolve_current_prompt()
        self.assertEqual(self.game.current_round(), 1)

    def test_SecondRound(self):
        self.game.resolve_current_prompt()
        self.game.resolve_current_prompt()
        self.assertEqual(self.game.current_round(), 2)

            
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

    def test_max_difficulty_blank(self):
        """Test that all prompts are available if max difficulty is not set

        """
        self.game = Game.objects.get(name='TestGame')
        prompts = self.game.availablePrompts()
        self.failUnlessEqual(Prompt.objects.count(), 16)
        #test that the prompt count equals the total number of prompts 
        #excluding those private to the other users
        #With 3 prompts private to the other user the prompt count for the game is thirteen
        self.failUnlessEqual(prompts.count(), 14)

    def test_max_difficulty(self):
        """Test that only sub-max prompts are displayed if a max difficulty is set
        """
        self.game = Game.objects.get(name='WimpyGame')
        prompts = self.game.availablePrompts()
        #test that the prompt count is 9
        self.failUnlessEqual(prompts.count(), 10)
        for prompt in prompts:
            self.failUnless(prompt.difficulty <= self.game.max_difficulty)

class TaggedItemTest(TestCase):
    """test that prompts with tags selected for the game are excluded from the available prompts
    create a fixture 
    ten prompts (1 tagged for nudity and 1 tagged as mature content)
    A game with tags for nudity and adult
    """
    def test_tagged_item(self):
        user = User.objects.create_user("testes", "test@emlprime.com", "test")
        Game.objects.create(name="TagsGame", user = user)
        self.game = Game.objects.get(name="TagsGame")
        self.game.tags.create(tag="nudity")
        self.game.tags.create(tag="mature content")
        for i in range(10):
            Prompt.objects.create(name="prompt %d" % i, difficulty=1, owner=user)
        p9 = Prompt.objects.get(id=9)
        p9.tags.create(tag="nudity")
        p10 = Prompt.objects.get(id=10)
        p10.tags.create(tag="mature content")
        prompts = self.game.availablePrompts()
        self.failUnlessEqual(Prompt.objects.count(), 10)
        # test that the available prompts for the game is 8
        self.failUnlessEqual(prompts.count(), 8)

class GameAuthenticationTest(TestCase):
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

class GameCreateViewTest(TestCase):
    """Test that rendered pages display correctly
    """
    fixtures = ["all_difficulties"]
    def setUp(self):
        """Initilaizes the client and logs the user in
        """
        self.client = Client()
        self.user = User.objects.get(username="laura")
        self.client.login(username="laura", password='laura')

    def test_objectList(self):
        """Test that the game object list displays the games
        """
        response = self.client.get('/game/')        
        self.assertContains(response, "TestGame")
        self.assertContains(response, "WimpyGame")

    def test_createObject(self):
        """Tests that a post containing game data creates a game object
        """
        games = Game.objects.filter(name="TestGame2")
        self.failUnlessEqual(games.count(), 0)
        response = self.client.post('/game/create/', {"name": "TestGame2"})
        self.failUnlessEqual(games.count(), 1)
        
    def test_viewDetail(self):
        """Tests that a get request displays the game form
        """
        response = self.client.get('/game/create/')
        self.assertContains(response, "Name:")
        self.assertContains(response, "Create Game")
        self.assertContains(response, "tags")
        self.assertContains(response, "nudity")
        self.assertContains(response, "Maximum Difficulty:")

class GameCreateAnonymousViewTest(TestCase):
    """Test that we can create a game anonymously
    """
    def setUp(self):
        self.client = Client()
    
    def test_createAnonymousGame(self):
        """Test that a user can create a game without logging in.
        """
        # given I don't have a game
        # and I am not logged in
        game_name = "AnonymousTestGame"
        games = Game.objects.filter(name=game_name)
        self.failUnlessEqual(games.count(), 0)

        # when I try to access the create page
        response = self.client.get('/game/create/')
        self.assertRedirects(response, '/game/quickstart/', status_code=302, target_status_code=200)

        # I should see the quickstart page
        response = self.client.get('/game/quickstart/')
        doc = BeautifulSoup(response.content)
        quickstart = doc.find(id="quickstart")
        self.failUnless(quickstart, "Could not find quickstart")

    def test_quickstart(self):
        """Test that a user who submits the quickstart game has an anonymous user created
        """ 
        response = self.client.post("/game/quickstart/")
        self.assertRedirects(response, '/game/create/', status_code=302, target_status_code=200)
    
    def test_clearAnonymousGame(self):
        self.given_completed_game()
        response = self.client.get(self.game.get_absolute_url() + "game_over/")
        doc = BeautifulSoup(response.content)
        element = doc.find(id="save_or_delete_anonymous_game")
        self.failUnless(element, "Could not find save or delete.")

        save_form = element.find(id="save_form")
        self.failUnless(save_form, "Could not find save form")

        delete_form = element.find(id="delete_form")
        self.failUnless(delete_form, "Could not find delete form")

    def test_saveAnonymousGame(self):
        self.given_completed_game()
        self.user.username.startswith("anonymous_")
        values = {"username": "new_username", "password": "new_password"}
        response = self.client.post(self.game.save_anonymous_game_url(), values)
        self.assertRedirects(response, '/game/', status_code=302, target_status_code=200)

        user = User.objects.get(id=self.user.id)
        self.assertEqual(values["username"], user.username)

    def test_failToSaveAnonymousGame(self):
        self.given_completed_game()
        self.user.username.startswith("anonymous_")
        values = {"username": "", "password": ""}
        response = self.client.post(self.game.save_anonymous_game_url(), values)
        self.assertFormError(response, "save_user_form", "username", "This field is required.")
        self.assertFormError(response, "save_user_form", "password", "This field is required.")
        

    def given_completed_game(self):
        self.client.post("/game/quickstart/")
        self.user = User.objects.get(username="anonymous_0010")
        self.game = Game.objects.create(name="TestGame", user=self.user)
        self.game.game_over()
        
        
class GameViewTest(TestCase):
    """Test that rendered pages display correctly
    """
    fixtures = ["all_difficulties"]
    def setUp(self):
        """Initilaizes the client and logs the user in
        """
        self.client = Client()
        self.user = User.objects.get(username="laura")
        self.client.login(username="laura", password='laura')
        self.game = Game.objects.get(name="TestGame")

        for player in ['alice', 'bob']:
            Player.objects.create(name=player, game=self.game)
        prompts = Prompt.objects.all()
        self.game.assign_prompts(prompts)        
        self.game.in_progress()

    def test_deleteObject(self):
        """Test that delete_object deletes a game object
        """
        response = self.client.post(self.game.get_absolute_url()+'delete/')
        games = Game.objects.filter(name="TestGame")
        self.failUnlessEqual(games.count(), 0)
        
    def test_beginGame(self):
        """Tests that a post will change the status to in_progress
        """
        game = Game.objects.get(name="WimpyGame")
        self.failUnlessEqual(game.status, "created")
        response = self.client.post(game.get_absolute_url()+'begin_game/')
        game = Game.objects.get(name="WimpyGame")        
        self.failUnlessEqual(game.status, "in_progress")

    def test_displayBeginGame(self):
        """Test that a form is displayed to start the game
        Test that the rules are displayed
        """
        response = self.client.get(self.game.get_absolute_url()+'begin_game/')
        self.assertContains(response, "Rules of the Game")
        self.assertContains(response, "begin_game")

    def test_displayChoice(self):
        """Test that a form is displayed presenting a choice
        """
        response = self.client.get(self.game.get_absolute_url()+'choice/')
        self.assertContains(response, "play/dare")
        self.assertContains(response, "play/truth")

    def test_displayPlayTruth(self):
        """Test that the correct prompt is displayed for the choice given
        Test that a form is displayed to wimp out or complete
        """
        response = self.client.get(self.game.get_absolute_url()+'play/truth/')
        self.assertContains(response, "I am a truth")
        self.assertContains(response, "complete")
        self.assertContains(response, "wimp_out")

    def test_displayPlayDare(self):
        """Test that the correct prompt is displayed for the choice given
        Test that a form is displayed to wimp out or complete
        """
        response = self.client.get(self.game.get_absolute_url()+'play/dare/')
        self.assertContains(response, "I am a dare")
        self.assertContains(response, "complete")
        self.assertContains(response, "wimp_out")

    def test_playComplete(self):
        """Test that the prompt is finished and the score of the player is changed
        """
        response = self.client.post(self.game.get_absolute_url()+'complete/')
        player = Player.objects.get(id=1)
        self.failUnlessEqual(player.score, 1)
        

    def test_playWimpOut(self):
        """Test that the prompt is finished and the score of the player is not changed
        """
        response = self.client.post(self.game.get_absolute_url()+'wimp_out/')
        player = Player.objects.get(id=2)
        self.failUnlessEqual(player.score, 0)

    def test_redirects(self):
        """Tests that the game's absolute url redirects to the right pages

        Each status has its own view.  We will increment the status 
        and confirm that the redirect goes to the right place
        """
        game = Game.objects.get(name="WimpyGame")
        response = self.client.get(game.get_absolute_url())
        self.assertRedirects(response, 'player/2/create/', status_code=302, target_status_code=200)
        for player in ['alice', 'bob']:
            Player.objects.create(name=player, game=game)
        game.players_added()
        response = self.client.get(game.get_absolute_url())
        self.assertRedirects(response, 'game/2/select_prompts/', status_code=302, target_status_code=200)
        game.assign_prompts(Prompt.objects.all()[:3])
        response = self.client.get(game.get_absolute_url())
        self.assertRedirects(response, 'game/2/begin_game/', status_code=302, target_status_code=200)
        game.in_progress()
        response = self.client.get(game.get_absolute_url())
        self.assertRedirects(response, 'game/2/choice/', status_code=302, target_status_code=200)
        while game.current_prompt():
            game.resolve_current_prompt()
        response = self.client.get(game.get_absolute_url())
        self.assertRedirects(response, 'game/2/game_over/', status_code=302, target_status_code=200)
        #testing that the game over page announces a winner
        response = self.client.get('/game/2/game_over/')
        self.assertContains(response, "The Winner Is alice")
        self.assertContains(response, "alice:")

