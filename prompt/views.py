from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from tod.prompt.models import Prompt

def index(request):
    template = "prompt/index.html"
    context = {'prompts':Prompt.objects.all()}
    return render_to_response(template, context, context_instance=RequestContext(request))
