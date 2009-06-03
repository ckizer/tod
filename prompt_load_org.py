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
tag_file = file('prompt/tags.txt')
tags = [tag.strip() for tag in tag_file]
me = User.objects.get(username="laura")

# for testing
#[p.delete() for p in Prompt.objects.all()]

difficulty = 1
prompts = []
prompt_WIP = {}
for row in reader:
    if not row.find(":") > 0:
        continue
    field, value = row.strip().split(":")
    if field.find("Difficulty") > 0:
        prompt_WIP["difficulty"] = int(value.strip())
    elif field.find("Truth") > 0:
        prompt_WIP["truth"] = value.strip()
    elif field.find("Dare") > 0:
        prompt_WIP["dare"] = value.strip()
    elif field.find("Tags") > 0:
        #get a list of tags or an empty list, if no tag_list is provided
        prompt_WIP["tag_values"] = [v.strip() for v in value.split(",")] if value else []
    else:
        prompt_WIP["name"] = value.strip()

    if prompt_WIP.has_key("truth") and prompt_WIP.has_key("dare"):
        prompts.append(prompt_WIP.copy())
        del prompt_WIP["truth"]
        del prompt_WIP["dare"]
        del prompt_WIP["name"]
        if prompt_WIP.has_key("tag_values"):
            del prompt_WIP["tag_values"]

for prompt in prompts:
    prompt_form = PromptForm(data=prompt, owner=me)
    #get a list of tags or an empty list, if no tag_list is provided
    if prompt_form.is_valid():
        #save the prompt if the form is valid
        current_prompt=prompt_form.save()
        current_prompt.publish()
        #loop over the available tags and see if they are specified
        if not prompt.has_key("tag_values"): continue
        for tag_value in prompt["tag_values"]:
            #if a tag is specified, add it to the prompt
            if tag_value in tags:
                current_prompt.tags.create(tag=tag_value)
    else:
        print row
        print prompt_form.errors

print Prompt.objects.all().count()

