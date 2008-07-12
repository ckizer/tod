from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext

from tod.player.models import Player
from tod.game.models import Game
from tod.player.forms import PlayerForm
from tod.common.decorators import http_response

@login_required
@http_response
def player_list(request, game_id):
    """Lists the player objects
    """
    game = get_object_or_404(Game, pk=game_id)
    players = game.players.all()
    if not players:
        return HttpResponseRedirect('/player/%d/create/' % game.id)
    template = "player/player_list.html"
    object_list = players
    return locals()

@login_required
@http_response
def create(request, game_id):
    """Creates the player object
    """
    game = get_object_or_404(Game, pk=game_id)
    template = "player/player_form.html"
    if request.method == "POST":
        form = PlayerForm()
        values = request.POST.copy()
        form = PlayerForm(values)
        if form.is_valid():
            player = form.save(commit=False)
            player.score = 0
            player.game = game
            player.save()
            return HttpResponseRedirect('/player/%d/' % game.id)
        else:
            errors = form.errors
            assert False
    else:
        form = PlayerForm()
    return locals()

@login_required
def delete(request, player_id):
    """Deletes a player object
    """
    player = get_object_or_404(Player, pk=player_id)
    game = player.game
    player.delete()
    return HttpResponseRedirect('/player/%d/' % game.id)

    
