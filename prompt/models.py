from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    
    content_object = generic.GenericForeignKey()

    class Meta:
        ordering = ["tag"]
        unique_together = (("tag", "object_id"),)
    
    def __unicode__(self):
        return self.tag

class Owner(models.Model):
    name = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

class Prompt(models.Model):
    name = models.CharField(max_length=50, unique = True)
    truth = models.TextField()
    dare = models.TextField()
    difficulty = models.IntegerField()
    private = models.BooleanField(default=True, editable = False)
    owner = models.ForeignKey(Owner, editable = False)

    tags = generic.GenericRelation(TaggedItem)

    class Meta:
        ordering = ['difficulty']

    def __unicode__(self):
        return self.name

