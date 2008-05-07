from django.db import models
from tod.prompt.models import Prompt, TaggedItem, generic
from django.contrib.auth.models import User

class Game(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('players_added', 'Players Added'),
        ('prompts_selected', 'Prompts Selected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        )
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices = STATUS_CHOICES, editable = False, default='created')
    max_difficulty = models.IntegerField(default=10, null=True, blank=True)
    user = models.ForeignKey(User)

    tags = generic.GenericRelation(TaggedItem)

    def __str__(self):
        return self.name

    def availablePrompts(self):
        availablePrompts = Prompt.objects.all()
        availablePrompts = Prompt.objects.exclude(private=True) | Prompt.objects.filter(owner=self.user)
        if self.max_difficulty:
            availablePrompts = availablePrompts.filter(difficulty__lte=self.max_difficulty)
        return availablePrompts
        #exclude other people's private prompts
        #exclude prompts with tagged items selected for the game
        #exclude prompts with difficulty levels greater than the max_difficulty

    def assign_prompts(self, prompts):
        for prompt in prompts:
            gp = GamePrompt(game = self, prompt = prompt)
            gp.save()
        self.status = "prompts_selected"
        self.save()
        return prompts

    def create_game(self, rounds_selected):
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
        return "/game/%d/" % self.id

    def players_added(self):
        self.status = "players_added"
        self.save()
        return self.status

    def in_progress(self):
        self.status = "in_progress"
        self.save()
        return self.status
    
    def current_prompt(self):
        prompts=self.gameprompt_set.filter(is_complete=False)
        if prompts.count():
            return prompts[0]
        return False
    
    def current_player(self):
        players = self.players.all()
        player_count = players.count()
        completed_prompt_count = self.gameprompt_set.filter(is_complete=True).count()
        player=players[completed_prompt_count % player_count]
        return player

    def game_over(self):
        self.status="completed"
        self.save()
        return self.status

class GamePrompt(models.Model):
    game = models.ForeignKey(Game, blank=True)
    prompt = models.ForeignKey(Prompt, blank=True)
    is_complete = models.BooleanField(default=False, blank=True)

    def complete(self):
        self.is_complete=True
        self.save()
        return self.prompt.difficulty
