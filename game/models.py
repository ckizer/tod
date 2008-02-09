from django.db import models
from tod.prompt.models import Prompt

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

    def __str__(self):
        return self.name

    def assign_prompts(self, prompts):
        for prompt in prompts:
            gp = GamePrompt(game = self, prompt = prompt)
            gp.save()
        self.status = "prompts_selected"
        self.save()
        return prompts

    def create_game(self, rounds):
        if not self.max_difficulty:
            self.max_difficulty = 10
            self.save()
        #determine the number of players
        number_of_players = self.players.count()
        #populate a two-dimensional list of prompts
        prompts={}
        for difficulty in range(self.max_difficulty):
            prompts[difficulty]=Prompt.objects.filter(difficulty=difficulty).iterator()
        assigned_rounds = 0
        assigned_prompts = []
        current_difficulty = 0
        #loop over difficulty level
        while assigned_rounds < rounds and prompts:
            print "assigned rounds:", assigned_rounds
        #if there are enough prompts for the number of players
            try:
                for i in range(number_of_players):
                    assigned_prompts.append(prompts.get(current_difficulty, iter([])).next())
                assigned_rounds+=1
        #otherwise delete the remaining prompts at that difficulty level
            except StopIteration:
                print "deleting:", current_difficulty
                if current_difficulty in prompts.keys():
                    del prompts[current_difficulty]
            current_difficulty += 1
            current_difficulty %= 10
        self.assign_prompts(assigned_prompts)
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
