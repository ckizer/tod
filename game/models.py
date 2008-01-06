from django.db import models

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

    def get_absolute_url(self):
        return "/game/%d/" % self.id

    def players_added(self):
        self.status = "players_added"
        self.save()
        return self.status
