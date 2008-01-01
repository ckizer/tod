from django.shortcuts import render_to_response
from django.template import RequestContext

def test(request):
    template = "test.html"
    context = {'status':'very, very bad'}
    return render_to_response(template, context, context_instance=RequestContext(request))
