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

class Prompt(models.Model):
    """Provides logic for truth and dare object used in gameplay
    """
    name = models.CharField(max_length=50, unique = True)
    truth = models.TextField()
    dare = models.TextField()
    difficulty = models.IntegerField()
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
