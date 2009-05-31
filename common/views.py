from django.shortcuts import render_to_response
from tod.common.forms import UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate

from tod.common.decorators import http_response

@http_response
def register(request):
    template = "registration/register.html"
    if request.method == "POST":
        values = request.POST.copy()
        
        registration_form = UserForm(values, password=values.get("password"))
        if registration_form.is_valid():
            user = registration_form.save()
            user = authenticate(username=values["username"], password=values['password'])
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        registration_form = UserForm()
    return locals()
