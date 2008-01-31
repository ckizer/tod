#!/usr/bin/python
import sys
import os
from os.path import dirname
sys.path.insert(0, dirname(os.getcwd()))
os.environ['DJANGO_SETTINGS_MODULE'] = 'tod.settings'

from tod.prompt.models import Prompt, TaggedItem

for prompt in Prompt.objects.all():
    print prompt, prompt.tags.all()
