from django.shortcuts import render_to_response
from django.template import RequestContext
from tod.forms import UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login

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

@http_response
def register(request):
    template = "registration/register.html"
    if request.method == "POST":
        values = request.POST.copy()
        form = UserForm(values)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(values['password'])
            user.save()
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = UserForm()
    return locals()

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
