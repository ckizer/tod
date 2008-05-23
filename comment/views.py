from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext

from tod.comment.models import Comment
from tod.comment.forms import CommentForm

@login_required
def create(request):
    """Creates the comment object
    """
    if request.method == "POST":
        values = request.POST.copy()
        form = CommentForm(values)
        if form.is_valid():
            comment = form.save()
            return HttpResponseRedirect(str(values['page']).strip())
        else:
            errors = form.errors

    return HttpResponseRedirect('/')


@login_required
def delete(request, comment_id):
    """Deletes a comment object
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    game = comment.game
    comment.delete()
    return HttpResponseRedirect('/comment/%d/' % game.id)

    

