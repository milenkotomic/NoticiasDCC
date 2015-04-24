# -*- coding: utf-8 -*-
from DCCNews.forms import LoginForm, SlideText, SlideImage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
# from bzrlib.transport.http._urllib2_wrappers import Request

# login_view: a partir del request que cuenta con los datos del form
# realiza la autentificación contra la base de datos. Si valida, lleva al index,
# de lo contrario, se mantiene en la página y muestra un mensaje de error.
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


# logout_view: a partir del request, que cuenta con el usuario, realiza el cierre de la sesión.
# Lleva al usuario a la página de inicio de sesión con un mensaje de exito.
def logout_view(request):
    logout(request)
    form = LoginForm()
    context = {'notify_message': 'Sesion cerrada con exito.', 'form': form}
    return render(request, 'DCCNews/login.html', context)

# index: TODO
@login_required()
def index(request):
    return render(request, 'DCCNews/index.html')


# select_template: TODO
def select_template(request):
    return render(request, 'DCCNews/template_selection.html')


# new_publication: TODO
@login_required()
def new_publication(request, template_id):
    if template_id == "1":
        form = SlideText()
    elif template_id == "2":
        form = SlideImage()
    return render(request, 'DCCNews/slide.html', {'form': form})



# edit_publication: TODO
@login_required()
def edit_publication(request, publicaction_id):
    return HttpResponse("Editar contenido")

#Busca una diapositiva: TODO  
@login_required()
def search_contenido(request):
    return render(request, 'DCCNews/template_search.html')

#Busca por evento: TODO  
#@login_required()
def search_contenido_evento(request):
    return render(request, 'DCCNews/template_search_evento.html')