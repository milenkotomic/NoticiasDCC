# -*- coding: utf-8 -*-
from DCCNews.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
def login_view(request):
    if request.POST:
        user = authenticate(username=request.POST['user'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                url = reverse('DCCNews.views.index')
                return HttpResponseRedirect(url)

        message = "Nombre de usuario o contraseña invalido."
        form = LoginForm(initial={'user': request.POST['user']})
        return render(request, 'DCCNews/login.html', {'form': form, 'error_message': message})

    form = LoginForm()
    return render(request, 'DCCNews/login.html', {'form': form})

def logout_view(request):
    logout(request)
    form = LoginForm()
    context = {'notify_message': 'Sesion cerrada con exito.', 'form': form}
    return render(request, 'DCCNews/login.html', context)

@login_required()
def index(request):
    return HttpResponse("Hello.")