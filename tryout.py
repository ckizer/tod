#!/usr/bin/python
import sys
import os
from os.path import dirname
sys.path.insert(0, dirname(os.getcwd()))
os.environ['DJANGO_SETTINGS_MODULE'] = 'tod.settings'

from tod.prompt.models import Prompt, TaggedItem

def assign_tags(prompt_id, tags):
    current_prompt=Prompt.objects.get(id=prompt_id)
    for current_tag in tags:
        current_prompt.tags.create(tag=current_tag)

assign_tags(1, ["exhibitionism", "nudity", "danger"])

for prompt in Prompt.objects.all():
    print prompt, prompt.tags.all()
