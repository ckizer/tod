#!/usr/bin/python
import sys
import os
from os.path import dirname
sys.path.insert(0, dirname(os.getcwd()))
os.environ['DJANGO_SETTINGS_MODULE'] = 'tod.settings'

import csv
from tod.prompt.forms import PromptForm
from tod.prompt.models import Prompt

reader = csv.DictReader(open("prompts.csv"))
print Prompt.objects.all().count()
tag_file = file('prompt/tags.txt')
tags = [tag.strip() for tag in tag_file]

for row in reader:
    prompt_form = PromptForm(row)
    #get a list of tags or an empty list, if no tag_list is provided
    tag_values = row['tag_list'].split(",") if row['tag_list'] else []
    if prompt_form.is_valid():
        #save the prompt if the form is valid
        current_prompt=prompt_form.save()
        #loop over the available tags and see if they are specified
        for tag in tags:
            if tag in tag_values:
                #if a tag is specified, add it to the prompt
                current_prompt.tags.create(tag=tag)
    else:
        print row
        print prompt_form.errors

print Prompt.objects.all().count()

