from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from tod.prompt.models import Prompt, TaggedItem, generic

STATUS_CHOICES = (
    ('created', 'Created'),
    ('players_added', 'Players Added'),
    ('prompts_selected', 'Prompts Selected'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    )

name_help = "Choose a name for your game."
max_difficulty_help = "Assign a maximum difficulty level to the game.  The maximum difficulty is inclusive, so if you choose 7, you will get prompts with difficulties of 1 through 7."

class Game(models.Model):
    """object to contain logic for grouping prompts and players into a game unit

    accept a list of players
    define a set of parameters for limiting prompts
    maintain relationship to selected prompts
    track the status of chosen prompts
    track a status to maintain persistent state
    determine relative player scores
    """
    name = models.CharField(max_length=50, help_text=name_help)
    status = models.CharField(max_length=50, choices = STATUS_CHOICES, editable = False, default='created')
    max_difficulty = models.IntegerField(default=10, null=True, blank=True, help_text=max_difficulty_help)
    user = models.ForeignKey(User)
    tags = generic.GenericRelation(TaggedItem)

    def __unicode__(self):
        return self.name

    def maximumRounds(self):
        """
        """
        player_count = self.players.count()
        if not player_count:
            return False
        return sum([int(round(len(prompts)/player_count)) for prompts in self.segmentedPrompts()])
    def segmentedPrompts(self):
        """ return the available prompts broken out by difficulty
        """
        if not self.max_difficulty:
            self.max_difficulty = 10
            self.save()
        prompts=[]
        for difficulty in range(1,self.max_difficulty+1):
            prompts.append([prompt for prompt in self.availablePrompts().filter(difficulty=difficulty)])
        return prompts

    def availablePrompts(self):
        """Provides the available prompts for a game based on chosen preferences
        """
        availablePrompts = Prompt.objects.all()
        #exclude other people's private prompts
        availablePrompts = Prompt.objects.exclude(private=True) | Prompt.objects.filter(owner=self.user)
        #exclude prompts with tagged items selected for the game
        tags = [t.tag for t in self.tags.all()]
        prompt_ct = ContentType.objects.get_for_model(Prompt.objects.all()[0])
        availablePrompts = availablePrompts.exclude(tags__tag__in = tags, tags__content_type=prompt_ct)
        #exclude prompts with difficulty levels greater than the max_difficulty
        if self.max_difficulty:
            availablePrompts = availablePrompts.filter(difficulty__lte=self.max_difficulty)
        return availablePrompts

    def assign_prompts(self, prompts):
        """Takes a list of prompts selected for the game and changes the game status to prompts_selected
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
        """
        #determine the number of players
        player_count = self.players.count()
        #populate a two-dimensional list of prompts
        available_prompts=self.availablePrompts()
        prompts = self.segmentedPrompts()
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
            #increments to the next highest difficulty up until 10, then sets back to 1
            current_difficulty = (current_difficulty + 1)%10
            prompts_available = False
            for difficulty in range(1,len(prompts)):
                if len(prompts[difficulty]) >= player_count:
                    prompts_available = True
                if prompts_available:
                    break
            
        self.assign_prompts(game_prompts)
        return True

    def get_absolute_url(self):
        """Return the absolute url for this object
        """
        return "/game/%d/" % self.id

    def players_added(self):
        """Changes the status to players_added
        """

        self.status = "players_added"
        self.save()
        return self.status

    def in_progress(self):
        """Changes the status to in_progress
        """
        self.status = "in_progress"
        self.save()
        return self.status
    
    def game_over(self):
        """Changes the status from in_progress to completed
        """
        self.status="completed"
        self.save()
        return self.status

    def current_prompt(self):
        """Returns the next incomplete prompt
        """
        prompts=self.gameprompt_set.filter(is_complete=False)
        if prompts.count():
            return prompts[0]
        self.game_over()
        return False
    
    def current_player(self):
        """returns the next player in the list
        """
        players = self.players.all()
        player_count = players.count()
        completed_prompt_count = self.gameprompt_set.filter(is_complete=True).count()
        player=players[completed_prompt_count % player_count]
        return player

    def resolve_current_prompt(self, resolution = "complete"):
        """Complete a prompt and update score accodingly
        """
        current_prompt = self.current_prompt()
        if current_prompt:
            current_player = self.current_player()
            score = current_prompt.complete()
            if resolution == "complete":
                current_player.update_score(score)
        return score

    def getWinners(self):
        """Defines the winner to list when the is game over
        """
        winners = []
        max_score = None
        for player in self.players.all().order_by("-score"):
            if not max_score:
                max_score = player.score
            if player.score < max_score:
                break
            winners.append(player)
        return winners

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
        """
        self.is_complete=True
        self.save()
        return self.prompt.difficulty
