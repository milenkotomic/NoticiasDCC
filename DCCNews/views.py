# -*- coding: utf-8 -*-
from DCCNews.forms import LoginForm, SlideText, SlideImage, EventForm, EventImage
from DCCNews.models import Publication, Type, Template, Priority, Text, Image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django import forms
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
@login_required
def index(request):
    return render(request, 'DCCNews/index.html')


# select_template: TODO
@login_required
def select_template(request):
    return render(request, 'DCCNews/template_selection.html')


# new_publication: TODO
@login_required
def new_slide(request, template_id):
    path_image = 'DCCNews/images/plantilla'+template_id+'.png'
    if request.POST:
        if template_id == "1":
            form = SlideText(request.POST)
        elif template_id == "2":
            form = SlideImage(request.POST, request.FILES)
        if form.is_valid():
            pub = Publication()
            pub.user_id = request.user
            pub.tag_id = form.cleaned_data['slide_type']
            pub.type_id = Type.objects.get(pk=1)
            pub.template_id = Template.objects.get(pk=template_id)
            pub.priority_id = Priority.objects.get(pk=1)
            pub.init_date = form.cleaned_data['start_circulation']
            pub.end_date = form.cleaned_data['end_circulation']
            pub.modification_user_id = request.user
            pub.save()
            if form.cleaned_data.get('title'):
                text = Text(text=form.cleaned_data['title'],
                            number=1,
                            publication_id=pub)
                text.save()

            if form.cleaned_data.get('subhead'):
                text = Text(text=form.cleaned_data['subhead'],
                            number=3,
                            publication_id=pub)
                text.save()

            if form.cleaned_data.get('body'):
                text = Text(text=form.cleaned_data['body'],
                            number=4,
                            publication_id=pub)
                text.save()
            if form.cleaned_data.get('image'):
                image = Image(image=request.FILES['image'],
                              number=1,
                              publication_id=pub)
                image.save()

            url = reverse(index)
            return HttpResponseRedirect(url)

        return render(request, 'DCCNews/slide.html', {'form': form, 'image': path_image, 'new': True})
    if template_id == "1":
        form = SlideText()
    elif template_id == "2":
        form = SlideImage()

    return render(request, 'DCCNews/slide.html', {'form': form, 'image': path_image, 'new': True})


# edit_publication: TODO
@login_required
def edit_slide(request, publication_id):
    pub = get_object_or_404(Publication, pk=publication_id)
    texts = pub.text_set.all()
    images = pub.image_set.all()
    path_image = 'DCCNews/images/plantilla'+str(pub.template_id.id)+'.png'
    if request.POST:
        if pub.template_id.id == 1:
            form = SlideText(request.POST)
        elif pub.template_id.id == 2:
            form = SlideImage(request.POST, request.FILES)

        if form.is_valid():
            pub.tag_id = form.cleaned_data['slide_type']
            pub.type_id = Type.objects.get(pk=1)
            pub.priority_id = Priority.objects.get(pk=1)
            pub.init_date = form.cleaned_data['start_circulation']
            pub.end_date = form.cleaned_data['end_circulation']
            pub.modification_user_id = request.user
            pub.save()

            if form.cleaned_data.get('title'):
                text = texts.filter(number=1).first()
                text.text = form.cleaned_data['title']
                text.save()

            if form.cleaned_data.get('subhead'):
                text = texts.filter(number=3).first()
                text.text = form.cleaned_data['subhead']
                text.save()

            if form.cleaned_data.get('body'):
                text = texts.filter(number=4).first()
                text.text = form.cleaned_data['body']
                text.save()

            if form.cleaned_data.get('image'):
                image = images.filter(number=1).first()
                image.image = request.FILES['image']
                image.save()

            return render(request, 'DCCNews/slide.html', {'form': form,
                                                          'image': path_image,
                                                          'mensaje': True})

    initial_data = {'title': texts.filter(number=1).first(),
                    'subhead': texts.filter(number=3).first(),
                    'body': texts.filter(number=4).first(),
                    'start_circulation': pub.init_date.strftime('%Y-%m-%dT%H:%M'),
                    'end_circulation': pub.end_date.strftime('%Y-%m-%dT%H:%M'),
                    'slide_type': pub.tag_id.id}

    if pub.template_id.id == 1:
        form = SlideText(initial_data)
    elif pub.template_id.id == 2:
        form = SlideImage(initial_data)

    return render(request, 'DCCNews/slide.html', {'form': form, 'image': path_image})


# new_event: TODO
@login_required
def new_event(request, template_id):
    path_image = 'DCCNews/images/evento'+template_id+'.png'
    if request.POST:
        if template_id == "1":
            form = EventForm(request.POST)
        elif template_id == "2":
            form = EventImage(request.POST, request.FILES)
        if form.is_valid():
            pub = Publication()
            pub.user_id = request.user
            pub.tag_id = form.cleaned_data['slide_type']
            pub.type_id = Type.objects.get(pk=2)
            pub.template_id = Template.objects.get(pk=template_id)
            pub.priority_id = Priority.objects.get(pk=1)
            pub.init_date = form.cleaned_data['start_circulation']
            pub.end_date = form.cleaned_data['end_circulation']
            pub.modification_user_id = request.user

            pub.save()

            text = Text(text=form.cleaned_data['name'],
                        number=1,
                        publication_id=pub)
            text.save()

            text = Text(text=form.cleaned_data['exhibitor'],
                        number=2,
                        publication_id=pub)
            text.save()

            text = Text(text=form.cleaned_data['date'],
                        number=3,
                        publication_id=pub)
            text.save()

            text = Text(text=form.cleaned_data['time'],
                        number=4,
                        publication_id=pub)
            text.save()

            text = Text(text=form.cleaned_data['place'],
                        number=5,
                        publication_id=pub)
            text.save()

            if form.cleaned_data.get('image'):
                image = Image(image=request.FILES['image'],
                              number=1,
                              publication_id=pub)
                image.save()

            url = reverse(index)
            return HttpResponseRedirect(url)

        form.fields['slide_type'].widget = forms.HiddenInput()
        return render(request, 'DCCNews/event.html', {'form': form, 'image': path_image, 'new': True})
    if template_id == "1":
        form = EventForm(initial={'slide_type': 3})
    elif template_id == "2":
        form = EventImage(initial={'slide_type': 3})

    form.fields['slide_type'].widget = forms.HiddenInput()

    return render(request, 'DCCNews/event.html', {'form': form, 'image': path_image, 'new': True})


# edit_event: TODO
@login_required
def edit_event(request, publication_id):
    pub = get_object_or_404(Publication, pk=publication_id)
    texts = pub.text_set.all()
    images = pub.image_set.all()
    path_image = 'DCCNews/images/evento'+str(pub.template_id.id)+'.png'
    if request.POST:
        if pub.template_id.id == 1:
            form = EventForm(request.POST)
        elif pub.template_id == 2:
            form = EventImage(request.POST, request.FILES)

        if form.is_valid():
            pub.tag_id = form.cleaned_data['slide_type']
            pub.type_id = Type.objects.get(pk=2)
            pub.priority_id = Priority.objects.get(pk=1)
            pub.init_date = form.cleaned_data['start_circulation']
            pub.end_date = form.cleaned_data['end_circulation']
            pub.modification_user_id = request.user
            print pub.init_date
            pub.save()
            if form.cleaned_data.get('name'):
                text = texts.filter(number=1).first()
                text.text = form.cleaned_data['name']
                text.save()

            if form.cleaned_data.get('exhibitor'):
                text = texts.filter(number=2).first()
                text.text = form.cleaned_data['exhibitor']
                text.save()

            if form.cleaned_data.get('date'):
                text = texts.filter(number=3).first()
                text.text = form.cleaned_data['date']
                text.save()

            if form.cleaned_data.get('time'):
                text = texts.filter(number=4).first()
                text.text = form.cleaned_data['time']
                text.save()

            if form.cleaned_data.get('place'):
                text = texts.filter(number=5).first()
                text.text = form.cleaned_data['place']
                text.save()

            if form.cleaned_data.get('image'):
                image = images.filter(number=1).first()
                image.image = request.FILES['image']
                image.save()

            return render(request, 'DCCNews/event.html', {'form': form,
                                                          'image': path_image,
                                                          'mensaje': True})

    initial_data = {'name': texts.filter(number=1).first(),
                    'exhibitor': texts.filter(number=2).first(),
                    'date': texts.filter(number=3).first(),
                    'time': texts.filter(number=4).first(),
                    'place': texts.filter(number=5).first(),
                    'start_circulation': pub.init_date.strftime('%Y-%m-%dT%H:%M'),
                    'end_circulation': pub.end_date.strftime('%Y-%m-%dT%H:%M'),
                    'slide_type': pub.tag_id.id}

    if pub.template_id.id == 1:
        form = EventForm(initial_data)
    elif pub.template_id.id == 2:
        form = EventImage(initial_data)

    form.fields['slide_type'].widget = forms.HiddenInput()

    return render(request, 'DCCNews/event.html', {'form': form, 'image': path_image})


# Busca una diapositiva: TODO
@login_required
def search_contenido(request):
    list = [] 
    Pubs = Publication.objects.order_by('-creation_date')
    
    for pub in Pubs:
        print(pub)
        texts = pub.text_set.all()
        p = {   "title" :  texts.first(),
                "tipe" : pub.tag_id.name,
                "id" : pub.pk,
             }
        list.append(p)
        
    return render(request, 'DCCNews/template_search.html', {"list" : list })


# Busca por evento: TODO
@login_required
def search_contenido_evento(request):
    list = [] 
    Pubs = Publication.objects.order_by('creation_date')[:5]
    
    for pub in Pubs:
        print(pub)
        texts = pub.text_set.all()
        p = {   "title" :  texts.first(),
                "tipe" : pub.tag_id.name,
                "id" : pub.pk,
             }
        list.append(p)

    return render(request, 'DCCNews/template_search_evento.html', {"list" : list })


def visualize(request):
    return render(request, 'DCCNews/visualization.html')

def template(request):
    return render(request, 'DCCNews/template1.html')
