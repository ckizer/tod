from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.newforms import form_for_model
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object
from django.views.generic.create_update import delete_object

from tod.game.models import Game
from tod.prompt.models import Prompt

@login_required
def limited_object_list(*args, **kwargs):
    return object_list(*args, **kwargs)

@login_required
def limited_create_object(*args, **kwargs):
    return create_object(*args, **kwargs)

@login_required
def limited_delete_object(*args, **kwargs):
    return delete_object(*args, **kwargs)

@login_required
def detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    #define a dictionary of redirects depending on the status of the game
    game_status = {
        'created': "/player/%s/" % game_id,
        'players_added': '/game/%s/select_prompts/' % game_id,
        'prompts_selected': '/game/%s/begin_game/' % game_id,
        'in_progress': '/game/%s/choice/' % game_id,
        'completed': '/game/%s/game_over/' % game_id,
        }

    return HttpResponseRedirect(game_status[game.status])

@login_required
def select_prompts(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    template = "game/select_prompts.html"
    player_count = game.players.count()
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
            game.create_game(rounds)
            return HttpResponseRedirect(game.get_absolute_url())
        else:
            if rounds<1:
                context["error"] = "MINIMUM_ROUNDS_EXCEEDED"
            else:
                context["error"] = "MAXIMUM_ROUNDS_EXCEEDED"
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def begin_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    rules = file("game/rules.txt").read()
    template = "game/begin_game.html"
    context = {"game": game, "rules": rules}
    if request.method == "POST":
        game.in_progress()
        return HttpResponseRedirect(game.get_absolute_url())
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def choice(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    template = "game/choice.html"
    if not game.current_prompt():
        game.game_over()
        return HttpResponseRedirect(game.get_absolute_url())
    current_prompt = game.current_prompt().prompt
    context = {"current_prompt": current_prompt, "current_game": game, "current_player": game.current_player()}
    return render_to_response(template, context, context_instance=RequestContext(request))
    
@login_required
def play(request, game_id, choice):
    game = get_object_or_404(Game, pk=game_id)
    template = "game/play.html"
    current_prompt = game.current_prompt().prompt
    description = current_prompt.truth if choice == "truth" else current_prompt.dare
    context = {"current_prompt": current_prompt, "current_game": game, "current_player": game.current_player(), "description": description}
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def wimp_out(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    current_prompt = game.current_prompt()
    current_prompt.complete()
    return HttpResponseRedirect(game.get_absolute_url())

@login_required
def complete(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    current_prompt = game.current_prompt()
    current_player = game.current_player()
    score = current_prompt.complete()
    current_player.update_score(score)
    return HttpResponseRedirect(game.get_absolute_url())

@login_required
def game_over(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    template = "game/over.html"
    context = {"players": game.players.all(), "game": game}
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def players_added(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    game.players_added()
    return HttpResponseRedirect(game.get_absolute_url())
