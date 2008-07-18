from django.shortcuts import render_to_response
from django.template import RequestContext
from tod.forms import UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate

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
        registration_form = UserForm(values)
        if registration_form.is_valid():
            user = registration_form.save(commit=False)
            user.set_password(values['password'])
            user.save()
            user = authenticate(username=values["username"], password=values['password'])
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        registration_form = UserForm()
    return locals()

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
