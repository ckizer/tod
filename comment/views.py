from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import send_mail

from tod.settings import SERVER_EMAIL
from tod.comment.models import Comment
from tod.comment.forms import CommentForm

def create(request):
    """Creates the comment object
    """
    if request.method == "POST":
        values = request.POST.copy()
        page = request.META['HTTP_REFERER'] if request.META.has_key('HTTP_REFERER') else '/'
        form = CommentForm(values, page=page)
        if form.is_valid():
            comment = form.save()
            message =  "%s\n%s\n%s\n%s" % (comment.page, comment.description, comment.email, comment.created)
            # try to send mail. If it fails print out an error
            try:
                send_mail('Truth or Dare Comment Submitted', message, comment.email, [SERVER_EMAIL], fail_silently=False)
            except:
                print "Error: could not send mail to admins"
            return HttpResponseRedirect(page)
        else:
            errors = form.errors
    return HttpResponseRedirect(page)


def delete(request, comment_id):
    """Deletes a comment object
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    game = comment.game
    comment.delete()
    return HttpResponseRedirect('/comment/%d/' % game.id)

    

