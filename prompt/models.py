from django.db import models

class Prompt(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    difficulty = models.IntegerField()

    class Meta:
        ordering = ['difficulty']

    def __str__(self):
        return self.name

