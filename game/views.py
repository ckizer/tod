
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.newforms import form_for_model

from tod.game.models import Game
from tod.prompt.models import Prompt

def detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    #define a dictionary of redirects depending on the status of the game
    game_status = {
        'created': "/player/%s/" % game_id,
        'players_added': '/game/%s/select_prompts/' % game_id,
        'prompts_selected': '/game/%s/begin_game/' % game_id,
        'in_progress': '/game/%s/play/' % game_id,
        'completed': '/game/%s/game_over/' % game_id,
        }

    return HttpResponseRedirect(game_status[game.status])

def select_prompts(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    template = "game/select_prompts.html"
    player_count = game.player_set.count()
    error = ""
    if player_count:
        maximum_rounds = Prompt.objects.count() / player_count
    else:
        maximum_rounds = 0
        error = "MINIMUM_PLAYERS_EXCEEDED"
    context = {"game": game, "maximum_rounds": maximum_rounds, "error": error}
    if request.method == "POST":
        values = request.POST.copy()
        rounds = int(values['rounds'])
        if 0 < rounds <= maximum_rounds:
            prompt_count = player_count*rounds
            prompts = Prompt.objects.filter(difficulty = 1)
            game.assign_prompts(prompts)
            return HttpResponseRedirect(game.get_absolute_url())
        else:
            if rounds<1:
                context["error"] = "MINIMUM_ROUNDS_EXCEEDED"
            else:
                context["error"] = "MAXIMUM_ROUNDS_EXCEEDED"
    return render_to_response(template, context, context_instance=RequestContext(request))

def begin_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    template = "game/begin_game.html"
    context = {"game": game, "rules": rules}
    if request.method == "POST":
        game.in_progress()
        return HttpResponseRedirect(game.get_absolute_url())
    return render_to_response(template, context, context_instance=RequestContext(request))

def play(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    template = "game/play.html"
    current_prompt = game.current_prompt()
    if not current_prompt:
        game.game_over()
        return HttpResponseRedirect(game.get_absolute_url())
    context = {"current_prompt": current_prompt.prompt, "current_game": game, "current_player": game.current_player()}
    return render_to_response(template, context, context_instance=RequestContext(request))

def wimp_out(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    current_prompt = game.current_prompt()
    current_prompt.complete()
    return HttpResponseRedirect(game.get_absolute_url())

def complete(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    current_prompt = game.current_prompt()
    current_player = game.current_player()
    score = current_prompt.complete()
    current_player.update_score(score)
    return HttpResponseRedirect(game.get_absolute_url())

def game_over(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    template = "game/over.html"
    context = {"players": game.player_set.all(), "game": game}
    return render_to_response(template, context, context_instance=RequestContext(request))

def players_added(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    game.players_added()
    return HttpResponseRedirect(game.get_absolute_url())
