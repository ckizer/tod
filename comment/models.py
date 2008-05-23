from django.db import models

from tod.game.models import Game

class Comment(models.Model):
    """Provides functionality for the comment object
    """
    page = models.CharField(max_length=50)
    description = models.TextField(help_text="Please describe the problem you're seeing.")
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True, null=False, blank=True, editable=False)
    
    def __unicode__(self):
        return self.page



