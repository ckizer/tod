from django.db import models
from django.contrib.auth.models import User

from tod.prompt.models import Prompt, TaggedItem, generic

STATUS_CHOICES = (
    ('created', 'Created'),
    ('players_added', 'Players Added'),
    ('prompts_selected', 'Prompts Selected'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    )

class Game(models.Model):
    """object to contain logic for grouping prompts and players into a game unit

    accept a list of players
    define a set of parameters for limiting prompts
    maintain relationship to selected prompts
    track the status of chosen prompts
    track a status to maintain persistent state
    determine relative player scores
    """
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices = STATUS_CHOICES, editable = False, default='created')
    max_difficulty = models.IntegerField(default=10, null=True, blank=True)
    user = models.ForeignKey(User)
    tags = generic.GenericRelation(TaggedItem)

    def __unicode__(self):
        return self.name

    def availablePrompts(self):
        """Provides the available prompts for a game based on chosen preferences

        TODO - test that other users' private prompts are excluded
        TODO - test that prompts exceeding the max difficulty are excluded
        TODO - test that prompts with tags selected for exclusion from the game are excluded
        """
        availablePrompts = Prompt.objects.all()
        #exclude other people's private prompts
        availablePrompts = Prompt.objects.exclude(private=True) | Prompt.objects.filter(owner=self.user)
        #exclude prompts with tagged items selected for the game
        tags = self.tags
        if tags:
            for tag in tags:
                availablePrompts = availablePrompts.exclude(tags = tag)
        #exclude prompts with difficulty levels greater than the max_difficulty
        if self.max_difficulty:
            availablePrompts = availablePrompts.filter(difficulty__lte=self.max_difficulty)
        return availablePrompts

    def assign_prompts(self, prompts):
        """Takes a list of prompts selected for the game and changes the game status to prompts_selected

        TODO - test that the game's status is changed to prompts_selected
        TODO - test that the prompts for the game are saved
        """
        for prompt in prompts:
            gp = GamePrompt(game = self, prompt = prompt)
            gp.save()
        self.status = "prompts_selected"
        self.save()
        return prompts

    def create_game(self, rounds_selected):
        """Arranges prompts for gameplay
             
        Takes the number of rounds selected and assigns equal-difficulty
        prompts within each round
        Stops when there are not enough prompts of any one difficulty to fill
        a whole round or when the rounds selected have been filled

        TODO - Test that all prompts in one round have the same difficulty
        TODO - Test that if there aren't enough prompts that we are short rounds
        TODO - Test that if there are enough prompts that we have the correct number of rounds
        """
        if not self.max_difficulty:
            self.max_difficulty = 10
            self.save()
        #determine the number of players
        player_count = self.players.count()
        #populate a two-dimensional list of prompts
        prompts=[]
        for difficulty in range(1,self.max_difficulty+1):
            prompts.append([prompt for prompt in Prompt.objects.filter(difficulty=difficulty)])
        rounds_assigned = 0
        game_prompts = []
        current_difficulty = 0
        prompts_available = True
        #loop over the difficulty levels and assign prompts to the game
        while rounds_selected > rounds_assigned and prompts_available:
            prompt_count = len(prompts[current_difficulty])

            if prompt_count >= player_count:
                for player in range(player_count):
                    game_prompts.append(prompts[current_difficulty].pop())
                rounds_assigned += 1

            current_difficulty = (current_difficulty + 1)%10
            prompts_available = False
            for difficulty in range(1,11):
                if len(prompts[current_difficulty]) >= player_count:
                    prompts_available = True
                if prompts_available:
                    break
            
        self.assign_prompts(game_prompts)
        return True

    def get_absolute_url(self):
        """Return the absolute url for this object

        TODO - Test that a game returns the correct absolute url
        """
        return "/game/%d/" % self.id

    def players_added(self):
        """Changes the status to players_added

        TODO - Test that the game's status changes from created to players_added
        """

        self.status = "players_added"
        self.save()
        return self.status

    def in_progress(self):
        """Changes the status to in_progress

        TODO - Test that the game's status changes from players_added to in_progress
        """
        self.status = "in_progress"
        self.save()
        return self.status
    
    def game_over(self):
        """Changes the status from in_progress to completed

        TODO - Test that status is changed from in_progress to completed
        """
        self.status="completed"
        self.save()
        return self.status

    def current_prompt(self):
        """Returns the next incomplete prompt
        
        TODO - Test that if there are prompts, that the next incomplete prompt is displayed
        TODO - Test that if the prompt is not completed or wimped that the same one displays
        TODO - Test that if there are no prompts remaining, that False is returned
        """
        prompts=self.gameprompt_set.filter(is_complete=False)
        if prompts.count():
            return prompts[0]
        return False
    
    def current_player(self):
        """returns the next player in the list

        TODO - Test that as prompts are completed the players are incremented in order.
        """
        players = self.players.all()
        player_count = players.count()
        completed_prompt_count = self.gameprompt_set.filter(is_complete=True).count()
        player=players[completed_prompt_count % player_count]
        return player

class GamePrompt(models.Model):
    """Many-To-Many relationship between Game and Prompt

    Tracks the prompts that have been assigned to this Game
    Tracks the status of prompts in the game so we know when the game is done
    """
    game = models.ForeignKey(Game, blank=True)
    prompt = models.ForeignKey(Prompt, blank=True)
    is_complete = models.BooleanField(default=False, blank=True)

    def complete(self):
        """Change the status so that is_complete is True

        TODO - Test that status is not complete before and is complete after.
        """
        self.is_complete=True
        self.save()
        return self.prompt.difficulty
