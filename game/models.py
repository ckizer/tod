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

    def __str__(self):
        return self.name

    def assign_prompts(self, prompts):
        for prompt in prompts:
            gp = GamePrompt(game = self, prompt = prompt)
            gp.save()
        self.status = "prompts_selected"
        self.save()
        return prompts

    def get_absolute_url(self):
        return "/game/%d/" % self.id

    def players_added(self):
        self.status = "players_added"
        self.save()
        return self.status

class GamePrompt(models.Model):
    game = models.ForeignKey(Game, blank=True)
    prompt = models.ForeignKey(Prompt, blank=True)
    is_complete = models.BooleanField(default=False, blank=True)

    def complete(self):
        self.is_complete=True
        self.save()
