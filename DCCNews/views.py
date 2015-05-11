# -*- coding: utf-8 -*-
from DCCNews.forms import LoginForm, SlideText, SlideImage, EventForm, EventImage, SearchSlide, SearchEvent
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
    template = get_object_or_404(Template, pk=template_id)
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

        return render(request, 'DCCNews/slide.html', {'form': form, 'image': template.view_prev, 'new': True})
    if template_id == "1":
        form = SlideText()
    elif template_id == "2":
        form = SlideImage()

    return render(request, 'DCCNews/slide.html', {'form': form, 'image': template.view_prev, 'new': True})


# edit_publication: TODO
@login_required
def edit_slide(request, publication_id):
    pub = get_object_or_404(Publication, pk=publication_id)
    template = get_object_or_404(Template, pk=pub.template_id.id)
    texts = pub.text_set.all()
    images = pub.image_set.all()
    # path_image = 'DCCNews/images/plantilla'+str(pub.template_id.id)+'.png'
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
                                                          'image': template.view_prev,
                                                          'mensaje': True})

    initial_data = {'title': texts.filter(number=1).first(),
                    'subhead': texts.filter(number=3).first(),
                    'body': texts.filter(number=4).first(),
                    'start_circulation': pub.init_date.strftime('%d-%m-%Y %H:%M'),
                    'end_circulation': pub.end_date.strftime('%d-%m-%Y %H:%M'),
                    'slide_type': pub.tag_id.id}

    if pub.template_id.id == 1:
        form = SlideText(initial_data)
    elif pub.template_id.id == 2:
        form = SlideImage(initial_data)

    return render(request, 'DCCNews/slide.html', {'form': form, 'image': template.view_prev})


# new_event: TODO
@login_required
def new_event(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    if request.POST:
        if template_id == "5":
            form = EventForm(request.POST)
        elif template_id == "6":
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
        return render(request, 'DCCNews/event.html', {'form': form, 'image': template.view_prev, 'new': True})
    if template_id == "5":
        form = EventForm(initial={'slide_type': 3})
    elif template_id == "6":
        form = EventImage(initial={'slide_type': 3})

    form.fields['slide_type'].widget = forms.HiddenInput()

    return render(request, 'DCCNews/event.html', {'form': form, 'image': template.view_prev, 'new': True})


# edit_event: TODO
@login_required
def edit_event(request, publication_id):
    pub = get_object_or_404(Publication, pk=publication_id)
    template = get_object_or_404(Template, pk=pub.template_id.id)
    texts = pub.text_set.all()
    images = pub.image_set.all()
    path_image = 'DCCNews/images/evento'+str(pub.template_id.id)+'.png'
    if request.POST:
        if pub.template_id.id == 5:
            form = EventForm(request.POST)
        elif pub.template_id == 6:
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

            form.fields['slide_type'].widget = forms.HiddenInput()
            return render(request, 'DCCNews/event.html', {'form': form,
                                                          'image': template.view_prev,
                                                          'mensaje': True})

    initial_data = {'name': texts.filter(number=1).first(),
                    'exhibitor': texts.filter(number=2).first(),
                    'date': texts.filter(number=3).first(),
                    'time': texts.filter(number=4).first(),
                    'place': texts.filter(number=5).first(),
                    'start_circulation': pub.init_date.strftime('%d-%m-%Y %H:%M'),
                    'end_circulation': pub.end_date.strftime('%d-%m-%Y %H:%M'),
                    'slide_type': pub.tag_id.id}

    if pub.template_id.id == 5:
        form = EventForm(initial_data)
    elif pub.template_id.id == 6:
        form = EventImage(initial_data)

    form.fields['slide_type'].widget = forms.HiddenInput()

    return render(request, 'DCCNews/event.html', {'form': form, 'image': template.view_prev})


# Busca una diapositiva: TODO
@login_required()
def search_slide(request):
    Pubs = Publication.objects.order_by('-creation_date').filter(type_id__name__icontains="slide")
    list = []
    # if this is a POST request we need to process the form data
    if request.POST:
        # create a form instance and populate it with data from the request:
        form = SearchSlide(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            titulo = form.cleaned_data['titulo']
            slide_type = form.cleaned_data['slide_type']
            #texts = Text.objects.filter(text__icontains=titulo)
            print(titulo)
            if form.cleaned_data.get('titulo'):
                Pubs = Pubs.filter(text__number__exact=1 ,text__text__icontains=titulo)
            print(slide_type)         
            if form.cleaned_data.get('slide_type'):
                Pubs = Pubs.filter(tag_id__name__icontains=slide_type)
            #Pubs = Pubs.filter
            #texts = Pubs.text_set.filter(name_icontains=titulo)
            #texts.filter();
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchSlide()    
    #Pubs = Pubs.distinct()
    #--- busqueda
    for pub in Pubs:
        #    print(pub)
        texts = pub.text_set.all()
        p = {   "title" :  texts.first(),
                "type" : pub.tag_id.name,
                "id" : pub.pk,
            }
        list.append(p)
            
    return render(request, 'DCCNews/template_search.html', {"list" : list , "form" : form} )


# Busca por evento: TODO
@login_required()
def search_event(request):
    list = [] 
    Pubs = Publication.objects.order_by('-creation_date').filter(type_id__name__icontains="event")
        # if this is a POST request we need to process the form data
    if request.POST:
        # create a form instance and populate it with data from the request:
        form = SearchEvent(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            titulo = form.cleaned_data['titulo']
            slide_type = form.cleaned_data['slide_type']
            expositor = form.cleaned_data['expositor']
            date = form.cleaned_data['date']
            #texts = Text.objects.filter(text__icontains=titulo)
            print(titulo)
            if form.cleaned_data.get('titulo'):
                Pubs = Pubs.filter(text__number__exact=1 , text__text__icontains=titulo)
                
            print(slide_type)         
            if form.cleaned_data.get('slide_type'):
                Pubs = Pubs.filter(tag_id__name__icontains=slide_type)
                
            print(expositor)
            if form.cleaned_data.get('expositor'):
                #Pubs = Pubs.filter(text__number=2)
                Pubs = Pubs.filter(text__number__exact=2 , text__text__icontains=expositor)
                
            print(date)
            if form.cleaned_data.get('date'):
                Pubs = Pubs.filter(text__number__exact=3 , text__text__icontains=date)
    else:
        form = SearchEvent()        
    #Pubs = Pubs.distinct()
    
    for pub in Pubs:
        print(pub)
        texts = pub.text_set.all()
        p = {   "title" :  texts.first(),
                "type" : pub.tag_id.name,
                "id" : pub.pk,
             }
        list.append(p)
        #"form" : form
    return render(request, 'DCCNews/template_search_evento.html', {"list" : list , "form" : form})

def visualize(request):
    return render(request, 'DCCNews/visualization2.html')

def template(request):
    return render(request, 'DCCNews/template1.html')
