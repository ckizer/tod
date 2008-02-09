from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.newforms import form_for_model

from tod.player.models import Player
from tod.game.models import Game

def player_list(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    players = game.players.all()
    if not players:
        return HttpResponseRedirect('/player/%d/create' % game.id)
    template = "player/player_list.html"
    context = {"object_list": players, "game": game}
    return render_to_response(template, context, context_instance=RequestContext(request))

def create(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    template = "player/player_form.html"
    PlayerForm = form_for_model(Player)
    if request.method == "POST":
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
    context = {"game": game, "form": PlayerForm()}
    return render_to_response(template, context, context_instance=RequestContext(request))

def delete(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    game = player.game
    player.delete()
    return HttpResponseRedirect('/player/%d/' % game.id)

    
