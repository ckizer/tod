from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from tod.prompt.models import Prompt

def index(request):
    template = "prompt/index.html"
    context = {'prompts':Prompt.objects.all()}
    return render_to_response(template, context, context_instance=RequestContext(request))

def play(request):
    template = "prompt/play.html"
    active_prompts = Prompt.objects.filter(is_complete=False)
    if not active_prompts:
        return HttpResponseRedirect("/prompt/game_over/")
    context = {"current_prompt":active_prompts[0]}
    return render_to_response(template, context, context_instance=RequestContext(request))

def complete(request, prompt_id):
    prompt = get_object_or_404(Prompt, pk=prompt_id)
    prompt.complete()
    return HttpResponseRedirect("/prompt/play/")

def reset(request):
    for prompt in Prompt.objects.all():
        prompt.reset()
    return HttpResponseRedirect("/prompt/play/")

def game_over(request):
    template = "prompt/game_over.html"
    context = {}
    return render_to_response(template, context, context_instance=RequestContext(request))
