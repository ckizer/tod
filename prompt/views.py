from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import delete_object
from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext

from tod.prompt.models import Prompt
from tod.prompt.forms import PromptForm
from tod.comment.forms import CommentForm

@login_required
def limited_object_list(*args, **kwargs):
    """Lists prompt object

    TODO - (defer) test that view provides prompt object list
    """
    return object_list(*args, **kwargs)

@login_required
def limited_delete_object(*args, **kwargs):
    """Deletes prompt object
    """
    return delete_object(*args, **kwargs)

@login_required
def index(request):
    """Index of prompt objects

    TODO - (defer) test that this lists prompt objects
    TODO - (defer) decide between object list and index to display prompts
    """
    prompts = Prompt.objects.exclude(private=True) | Prompt.objects.filter(owner=request.user)
    comment_form = CommentForm(initial={'page': '/prompt/'})
    return render_to_response("prompt/index.html", locals(), context_instance=RequestContext(request))

@login_required
def detail(request):
    """Creates a prompt object using form input

    TODO - (defer) move post functionality into Prompt Form
    TODO - (defer) separate form processing into function
    """
    template = "prompt/prompt_detail.html"
    tag_file = file('prompt/tags.txt')
    tags = [tag.strip() for tag in tag_file]
    context = {'tags':tags}
    if request.method == 'POST':
        values = request.POST.copy()
        form = PromptForm(values)
        if form.is_valid():
            current_prompt=form.save(commit=False)
            current_prompt.owner=request.user
            current_prompt.save()
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
