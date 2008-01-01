from django.db import models

class Prompt(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    difficulty = models.IntegerField()
    is_complete = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ['difficulty']

    def __str__(self):
        return self.name

    def complete(self):
        self.is_complete=True
        self.save()

    def reset(self):
        self.is_complete=False
        self.save()
