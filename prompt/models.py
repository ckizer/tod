from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

class TaggedItem(models.Model):
    """Makes tag generic objects for relating prompt content and game preference
    """

    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    
    content_object = generic.GenericForeignKey()

    class Meta:
        ordering = ["tag"]
        unique_together = (("tag", "object_id"),)
    
    def __unicode__(self):
        return self.tag
name_help = "Give your prompt a descriptive and unique name, since the name will be displayed in the game"
truth_help = "Provide a challenge where the player has to tell the truth about something for when a player gets your prompt and chooses Truth"
dare_help = "Provide a challenge where the player has to do something potentially embarassing or difficult for when a player gets your prompt and chooses Dare"
difficulty_help = "Assign a difficulty to the prompt."

class Prompt(models.Model):
    """Provides logic for truth and dare object used in gameplay
    """
    name = models.CharField(max_length=100, unique = True, help_text=name_help)
    truth = models.TextField(help_text=truth_help)
    dare = models.TextField(help_text=dare_help)
    difficulty = models.IntegerField(help_text=difficulty_help)
    private = models.BooleanField(default=True, editable = False)
    owner = models.ForeignKey(User, editable = False)

    #Allows the prompts to be marked for content so the game can exclude them 
    tags = generic.GenericRelation(TaggedItem)

    class Meta:
        ordering = ['difficulty']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the absolute url for the prompt
        """
        return "/prompt/%d/" % self.id
