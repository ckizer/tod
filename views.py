from django.shortcuts import render_to_response
from django.template import RequestContext
from tod.forms import UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login

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
    context = {'form': form}
    return render_to_response(template, context, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
