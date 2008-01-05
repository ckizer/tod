from django.shortcuts import render_to_response
from django.template import RequestContext


def test(request):
    template = "test.html"
    context = {'status':'very, very bad'}
    return render_to_response(template, context, context_instance=RequestContext(request))

def mockups(request):
    template = "mockups.html"
    
    mockups = []
    for mock in file("mockups.txt"):
        mockups.append(mock.strip())
    context = {'mockups': mockups}
    return render_to_response(template, context, context_instance=RequestContext(request))
