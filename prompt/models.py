from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

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

class Prompt(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    difficulty = models.IntegerField()

    tags = generic.GenericRelation(TaggedItem)

    class Meta:
        ordering = ['difficulty']

    def __unicode__(self):
        return self.name

