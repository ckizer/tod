from datetime import datetime
from tod.settings import SITE_ROOT

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.create_update import delete_object

from tod.game.forms import GameForm
from tod.comment.forms import CommentForm
from tod.game.models import Game
from tod.prompt.models import Prompt
from tod.common.forms import UserForm
from tod.common.decorators import http_response, active_game

@login_required
@http_response
def object_list(request):
    """displays a list of game objects
    """
    template = "game/game_list.html"
    object_list = request.user.game_set.all()
    return locals()


@http_response
def create_object(request):
    """creates a game object if there is a post, otherwise displays the game form
    """
    user = request.user
    if user.is_anonymous():
        return HttpResponseRedirect("/game/quickstart/")
    if request.method == "POST":
        form = GameForm(data=request.POST.copy(), user=user)
        if form.is_valid():
            game = form.save()
            return HttpResponseRedirect(game.get_absolute_url())
    else:
        form = GameForm()
    template = "game/game_form.html"
    tag_file = file(SITE_ROOT + '/prompt/tags.txt')
    tags = [tag.strip() for tag in tag_file]
    return locals()

@http_response
def quickstart(request):
    """gives the user a choice between login in and creating an anonymous game
    """
    if request.method == "POST":
        anonymous_users = User.objects.filter(username__startswith="anonymous").order_by("-username")
        if anonymous_users.count():
            last_number = anonymous_users[0].username.split("_")[-1]
            if last_number.isdigit():
                username = "anonymous_%04d" % (int(last_number) + 1)
            else:
                username = "anonymous_0010"
        else:
            username = "anonymous_0010"
        values = {
            "username": username,
            "password": "ilovelaura"
            }
        form = UserForm(values, password=values.get("password"))
        if form.is_valid():
            user = form.save()
            user = authenticate(username=values["username"], password=values['password'])
            login(request, user)
        return HttpResponseRedirect("/game/create/")
        
    template = "game/quickstart.html"
    return locals()

@login_required
def limited_delete_object(*args, **kwargs):
    """generic delete limited by login
    """
    return delete_object(*args, **kwargs)


@login_required
def detail(request, game_id):
    """tells game where to redirect according to game status

    TODO - (defer) use named urls to avoid violating the DRY principle
    """
    game = get_object_or_404(Game, pk=game_id)
    #define a dictionary of redirects depending on the status of the game
    game_status = {
        'created': "/player/%s/create/" % game_id,
        'players_added': '/game/%s/select_prompts/' % game_id,
        'prompts_selected': '/game/%s/begin_game/' % game_id,
        'in_progress': '/game/%s/choice/' % game_id,
        'completed': '/game/%s/game_over/' % game_id,
        }
    return HttpResponseRedirect(game_status[game.status])

@login_required
@http_response
def select_prompts(request, game_id):
    """chooses which prompts are assigned to the game
    
    determine the number of rounds
    determine filtering rules by tag
    determine max_difficulty
    TODO - (defer) put filtering functionality into the model
    """
    game = get_object_or_404(Game, pk=game_id)

    template = "game/select_prompts.html"
    player_count = game.players.count()
    error = ""
    if player_count < 1:
        error = "MINIMUM_PLAYERS_EXCEEDED"
    maximum_rounds = game.maximumRounds()
    if request.method == "POST":
        values = request.POST.copy()
        rounds = int(values['rounds']) if values['rounds'] else 0
        if type(rounds)==int:
            if 0 < rounds <= maximum_rounds:
                game.create_game(rounds)
                return HttpResponseRedirect(game.get_absolute_url())
            else:
                error = "MINIMUM_ROUNDS_EXCEEDED" if rounds < 1 else "MAXIMUM_ROUNDS_EXCEEDED"
        else:
            error = "ROUNDS_NOT_INT"
    return locals()

@login_required
@http_response
def begin_game(request, game_id):
    """Displays game rules and gives a form to start the game

    a post will change the game status
    """
    game = get_object_or_404(Game, pk=game_id)
    rules = file(SITE_ROOT + "/game/rules.txt").read()
    template = "game/begin_game.html"
    if request.method == "POST":
        game.in_progress()
        return HttpResponseRedirect(game.get_absolute_url())
    return locals()

@login_required
@http_response
def choice(request, game_id):
    """Displays the truth or dare choice
    """
    game = get_object_or_404(Game, pk=game_id)
    template = "game/choice.html"
    if not game.current_prompt():
        return HttpResponseRedirect(game.get_absolute_url())
    current_prompt = game.current_prompt().prompt
    current_game = game
    current_player = game.current_player()
    current_round = game.current_round()
    return locals()
    
@login_required
@http_response
def play(request, game_id, choice):
    """Displays the prompt with the given choice and a form for finishing the prompt
    """
    game = get_object_or_404(Game, pk=game_id)
    if game.status=='completed':
        return HttpResponseRedirect(game.get_absolute_url())        
    template = "game/play.html"
    current_prompt = game.current_prompt().prompt
    description = current_prompt.truth if choice == "truth" else current_prompt.dare
    current_game = game
    current_player = game.current_player()
    return locals()

@login_required
def wimp_out(request, game_id):
    """Finishes the prompt without adding to the score
    """
    game = get_object_or_404(Game, pk=game_id)
    game.resolve_current_prompt("wimp out")
    return HttpResponseRedirect(game.get_absolute_url())

@active_game
@login_required
def complete(request, game_id):
    """Finishes the prompt and updates the player's score
    """
    game = get_object_or_404(Game, pk=game_id)
    game.resolve_current_prompt("complete")
    
    return HttpResponseRedirect(game.get_absolute_url())

@login_required
@http_response
def game_over(request, game_id):
    """Displays the game over page and the winner
    """
    game = get_object_or_404(Game, pk=game_id)
    players = game.players.all()
    winners = game.getWinners()
    if request.user.username.startswith("anonymous_"):
        is_anonymous = True  
        request.user.password = ""
        save_user_form = UserForm()
    else:
        is_anonymous = False
    template = "game/over.html"
    return locals()

@login_required
@http_response
def save_anonymous_game(request, game_id):
    """Saves the game with a new username and password
    """
    game = get_object_or_404(Game, pk=game_id)
    if request.method == "POST":
        values = request.POST.copy()

        save_user_form = UserForm(values, instance=request.user, password=values.get("password"))
        if save_user_form.is_valid():
            user = save_user_form.save()
            user = authenticate(username=values["username"], password=values['password'])
            login(request, user)
            return HttpResponseRedirect("/game/")
        else:
            players = game.players.all()
            winners = game.getWinners()
    is_anonymous = True if request.user.username.startswith("anonymous_") else False
    template = "game/over.html"
    return locals()

@login_required
@http_response
def delete_anonymous_game(request, game_id):
    """Deletes the game with a new username and password
    """
    game = get_object_or_404(Game, pk=game_id)
    if request.method == "POST":
        request.user.delete()
        return HttpResponseRedirect("/accounts/logout/")
    return HttpResponseRedirect("/accounts/logout/")

@login_required
def players_added(request, game_id):
    """Changes game status to players_added
    """
    game = get_object_or_404(Game, pk=game_id)
    game.players_added()
    return HttpResponseRedirect(game.get_absolute_url())
