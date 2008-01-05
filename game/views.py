from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.newforms import form_for_model

from tod.game.models import Game
from tod.prompt.models import Prompt

def select_prompts(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    template = "game/select_prompts.html"
    player_count = game.player_set.count()
    if player_count:
        rounds = Prompt.objects.count() / player_count
    context = {"game": game, "rounds": rounds}
    return render_to_response(template, context, context_instance=RequestContext(request))

def play(request):
    template = "game/play.html"
    active_prompts = Prompt.objects.filter(is_complete=False)
    if not active_prompts:
        return HttpResponseRedirect("/game/game_over/")
    context = {"current_prompt":active_prompts[0]}
    return render_to_response(template, context, context_instance=RequestContext(request))

def game_over(request):
    template = "game/over.html"
    context = {}
    return render_to_response(template, context, context_instance=RequestContext(request))
