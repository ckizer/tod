#!/usr/bin/python
import sys
import os
from os.path import dirname
sys.path.insert(0, dirname(os.getcwd()))
os.environ['DJANGO_SETTINGS_MODULE'] = 'tod.settings'
from django.contrib.auth.models import User

from tod.prompt.forms import PromptForm
from tod.prompt.models import Prompt

reader = open("prompts.org")
print Prompt.objects.all().count()
me = User.objects.get(username="laura")
[p.delete() for p in Prompt.objects.all()]

difficulty = 1
prompts = []
prompt_WIP = {}
for row in reader:
    if not row.find(":") > 0:
        continue
    field, value = row.strip().split(":")
    if field.find("Difficulty") > 0:
        prompt_WIP["difficulty"] = int(value.strip())
        continue
    if field.find("Truth") > 0:
        prompt_WIP["truth"] = value.strip()
        continue
    if field.find("Dare") > 0:
        prompt_WIP["dare"] = value.strip()
        continue
    prompt_WIP["name"] = value.strip()

    if prompt_WIP.has_key("truth") and prompt_WIP.has_key("dare"):
        prompts.append(prompt_WIP.copy())
        del prompt_WIP["truth"]
        del prompt_WIP["dare"]
        del prompt_WIP["name"]

print prompts
    

for prompt in prompts:
    prompt_form = PromptForm(data=prompt, owner=me)
    #get a list of tags or an empty list, if no tag_list is provided
    if prompt_form.is_valid():
        #save the prompt if the form is valid
        current_prompt=prompt_form.save()
        current_prompt.publish()
    else:
        print row
        print prompt_form.errors

print Prompt.objects.all().count()

