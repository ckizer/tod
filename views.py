from django.http import HttpResponseRedirect
from django.contrib.auth import logout

from tod.common.decorators import http_response

@http_response
def index(request):
    template = "home.html"
    return locals()

@http_response
def test(request):
    template = "test.html"
    status='very, very bad'
    return locals()

@http_response
def mockups(request):
    template = "mockups.html"
    mockups = []
    for mock in file("mockups.txt"):
        mockups.append(mock.strip())
    return locals()


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
