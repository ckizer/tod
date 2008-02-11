#!/usr/bin/python
import sys
import os
from os.path import dirname
sys.path.insert(0, dirname(os.getcwd()))
os.environ['DJANGO_SETTINGS_MODULE'] = 'tod.settings'

from tod.prompt.models import Prompt, TaggedItem

player_count = 2
rounds_selected = 1

rounds_assigned = 0
prompts_available = True
all_prompts = Prompt.objects.all()
prompts = []
for difficulty in range(1,11):
    prompts.append([prompt for prompt in Prompt.objects.filter(difficulty=difficulty)])
current_difficulty = 1
game_prompts = []

for level in prompts:
    print "*"*len(level)

#loop goes through the list of prompts as long as rounds_assigned
#is less than rounds_selected and as long as promts_available 
while rounds_selected > rounds_assigned and prompts_available:
    
    prompt_count = len(prompts[current_difficulty])

    #assign a round to the game, with one prompt for each player in player_count
    #the round comes from current_difficulty
    #as long as the prompt_count for current_difficulty
    #is greater than or equal to player_count
    #the assigned prompts are deleted from the list  
    #add one to rounds_assigned

    if prompt_count >= player_count:
        for player in range(player_count):
            game_prompts.append(prompts[current_difficulty].pop())
        rounds_assigned += 1

    #increment difficulty by one
    current_difficulty += 1
    
#check to see whether there are enough prompts in any difficulty
#level for another round.  if not, prompts_available = False
    prompts_available = False
    for difficulty in range(1,11):
        if len(prompts[current_difficulty]) >= player_count:
            prompts_available = True
        if prompts_available:
            break


print "game_prompts", game_prompts
print "round_assigned", rounds_assigned
