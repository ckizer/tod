from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.create_update import delete_object

from tod.game.forms import GameForm
from tod.game.models import Game
from tod.prompt.models import Prompt

@login_required
def object_list(request):
    """displays a list of game objects

    TODO - test that game objects are displayed
    """
    template = "game/game_list.html"
    context = {'object_list':request.user.game_set.all()}
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def create_object(request):
    """creates a game object if there is a post, otherwise displays the game form

    TODO - test that object is created if there is a post
    TODO - test that game form displays if there is not a post
    """
    if request.method == "POST":
        form = GameForm(user=request.user, data=request.POST.copy())
        if form.is_valid():
            game = form.save(commit=False)
            game.user = request.user
            game.save()
            return HttpResponseRedirect(game.get_absolute_url())
    else:
        form = GameForm()
    template = "game/game_form.html"
    return render_to_response(template, locals(), context_instance=RequestContext(request))

@login_required
def limited_delete_object(*args, **kwargs):
    """generic delete limited by login

    TODO - test that object is deleted
    """
    return delete_object(*args, **kwargs)

@login_required
def detail(request, game_id):
    """tells game where to redirect according to game status

    TODO - test that games with each status will redirect to the correct url's
    TODO - use named urls to avoid violating the DRY principle
    """
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
    """chooses which prompts are assigned to the game
    
    determine the number of rounds
    determine filtering rules by tag
    determine max_difficulty
    TODO - put filtering functionality into the model
    """
    game = get_object_or_404(Game, pk=game_id)

    template = "game/select_prompts.html"
    player_count = game.players.count()
    error = ""
    #TODO - availablePrompts instead of Prompt.objects.count()
    if player_count:
        maximum_rounds = Prompt.objects.count() / player_count
    else:
        maximum_rounds = 0
        error = "MINIMUM_PLAYERS_EXCEEDED"
    if request.method == "POST":
        values = request.POST.copy()
        rounds = int(values['rounds'])
        if 0 < rounds <= maximum_rounds:
            game.create_game(rounds)
            return HttpResponseRedirect(game.get_absolute_url())
        else:
            if rounds<1:
                error = "MINIMUM_ROUNDS_EXCEEDED"
            else:
                error = "MAXIMUM_ROUNDS_EXCEEDED"
    return render_to_response(template, locals(), context_instance=RequestContext(request))

@login_required
def begin_game(request, game_id):
    """Displays game rules and gives a form to start the game

    a post will change the game status
    TODO - test that a post will change the game status to in_progress
    TODO - test that a form is displayed to start the game
    TODO - test that the rules are displayed
    """
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
    """Displays the truth or dare choice

    sends to game over page if there are no more prompts
    TODO - test that an in progress game redirects to game over if there are no more prompts
    TODO - test that an in progress game's status is changed to game_over if there are no more prompts
    TODO - test that a form is displayed presenting a choice
    """
    game = get_object_or_404(Game, pk=game_id)
    template = "game/choice.html"
    if not game.current_prompt():
        return HttpResponseRedirect(game.get_absolute_url())
    current_prompt = game.current_prompt().prompt
    context = {"current_prompt": current_prompt, "current_game": game, "current_player": game.current_player()}
    return render_to_response(template, context, context_instance=RequestContext(request))
    
@login_required
def play(request, game_id, choice):
    """Displays the prompt with the given choice and a form for finishing the prompt

    TODO - test that the correct prompt is displayed for the choice given
    TODO - test that a form is displayed to wimp out or complete
    """
    game = get_object_or_404(Game, pk=game_id)
    template = "game/play.html"
    current_prompt = game.current_prompt().prompt
    description = current_prompt.truth if choice == "truth" else current_prompt.dare
    context = {"current_prompt": current_prompt, "current_game": game, "current_player": game.current_player(), "description": description}
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def wimp_out(request, game_id):
    """Finishes the prompt without adding to the score

    TODO - test that the prompt is finished and the score of the player is not changed
    """
    game = get_object_or_404(Game, pk=game_id)
    game.resolve_current_prompt("wimp out")
    return HttpResponseRedirect(game.get_absolute_url())

@login_required
def complete(request, game_id):
    """Finishes the prompt and updates the player's score

    TODO - test that the prompt is finished and the score of the player is changed
    """
    game = get_object_or_404(Game, pk=game_id)
    game.resolve_current_prompt("complete")
    return HttpResponseRedirect(game.get_absolute_url())

@login_required
def game_over(request, game_id):
    """Displays the game over page and the winner

    TODO - test that the game over page is displayed
    TODO - test that the winner is displayed
    """
    game = get_object_or_404(Game, pk=game_id)
    template = "game/over.html"
    context = {"players": game.players.all(), "game": game}
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def players_added(request, game_id):
    """Changes game status to players_added

    TODO - test that game status is changed to players_added
    """
    game = get_object_or_404(Game, pk=game_id)
    game.players_added()
    return HttpResponseRedirect(game.get_absolute_url())
