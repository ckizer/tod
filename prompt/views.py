from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from tod.prompt.models import Prompt
from tod.prompt.forms import PromptForm

def index(request):
    template = "prompt/index.html"
    context = {'prompts':Prompt.objects.all()}
    return render_to_response(template, context, context_instance=RequestContext(request))

def detail(request):
    template = "prompt/prompt_detail.html"
    tag_file = file('prompt/tags.txt')
    tags = [tag.strip() for tag in tag_file]
    context = {'tags':tags}
    if request.method == 'POST':
        values = request.POST.copy()
        form = PromptForm(values)
        if form.is_valid():
            current_prompt=form.save()
            for tag in tags:
                if values.get(tag,None):
                    current_prompt.tags.create(tag=tag)
            return HttpResponseRedirect("/prompt/")
        else:
            context['errors']=form.errors
    else:
        form = PromptForm()
        
    context['form']=form
    return render_to_response(template, context, context_instance=RequestContext(request))
