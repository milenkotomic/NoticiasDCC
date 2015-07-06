# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import time
from DCCNews.forms import LoginForm, SlideText, SlideImage, EventForm, EventImage, SearchSlide, SearchEvent, \
    SlideGraduation, SlideImageText, TagCreationForm, PublicationForm
from DCCNews.models import Publication, Type, Template, Priority, Text, Image, Temp, Tag
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import HiddenInput
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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

        message = "Nombre de usuario o contraseña inválido."
        form = LoginForm(initial={'user': request.POST['user']})
        return render(request, 'DCCNews/login.html', {'form': form, 'error_message': message})

    if request.user.is_active:
        url = reverse('DCCNews.views.index') + "?login=1"
        return HttpResponseRedirect(url)

    form = LoginForm()
    return render(request, 'DCCNews/login.html', {'form': form})


# logout_view: a partir del request, que cuenta con el usuario, realiza el cierre de la sesión.
# Lleva al usuario a la página de inicio de sesión con un mensaje de exito.
def logout_view(request):
    logout(request)
    form = LoginForm()
    context = {'notify_message': 'Sesión cerrada con éxito.', 'form': form}
    return render(request, 'DCCNews/login.html', context)


# index: a partir del request se redirige a la pagina de inicio. Recibe por GET los parametros create y login,
# de modo de mostrar los mensajes de alerta correspondientes
@login_required
def index(request):
    context = {}
    if request.GET.get('create'):
        context['create'] = True
    elif request.GET.get('login'):
        context['login'] = True
    c = RequestContext(request, context)
    return render_to_response('DCCNews/index.html', c)


# select_template: a partir del request redirige a la página para la elección del tipo de contenido a crear y
# la plantilla que se utilizará para crearlo
@login_required
def select_template(request):
    return render(request, 'DCCNews/template_selection.html')


# create_tag: a partir del formulario enviado mediante AJAX, se crea el nuevo tag. Se verifica que no exista
# un tag previo con el mismo nombre. La respuesta corresponde a un JSON con el mensaje a mostrar en el alert y la
# nueva renderización del select para tag.
def create_tag(request):
    new_tag = request.POST.get("new_tag", False)
    response = "Nuevo tag inválido"
    if new_tag and str(new_tag).replace(" ", "") != "":
        if Tag.objects.all().filter(name__iexact=new_tag).exists():
            response = "Tag ya existente"
        else:
            tag = Tag(name=new_tag)
            tag.save()
            response = "Tag agregado exitosamente"

    form = PublicationForm()
    data = {'text': response,
            'tags': render_to_response("DCCNews/tags.html", {"form": form}).content}
    return JsonResponse(data)


# delete_tag: a partir del formulario enviado mediante AJAX, se elimina un tag. Se verifica que no pertenzca a la lista
# de tags protegidos. La respuesta corresponde a un JSON con el mensaje a mostrar en el alert y la
# nueva renderización del select para tag.
def delete_tag(request):
    if request.POST:
        tag = request.POST.get("tag", False)
        no_delete_tags = [1, 2, 3, 4, 5]
        deleted_tag = False

        if tag and int(tag) not in no_delete_tags:
            tag = get_object_or_404(Tag, pk=int(tag))
            tag.delete()
            deleted_tag = True

        form = PublicationForm()
        data = {"tags": render_to_response("DCCNews/tags.html", {"form": form}).content,
                "deleted_tag": deleted_tag}
        return JsonResponse(data)


# new_slide: vista que cumple los siguientes roles:
# Mostrar el formulario para el ingreso de una nueva diapositiva a almacenar en el sistema
# Si recibe datos por POST, verifica que sean los datos correctos, si no son validos, se vuelve al formulario
# con los mensajes de error correspondietens. Si los datos valiadan, se vuelve a la página de inicio previo
# almacenamiento de los datos.
@login_required
def new_slide(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    if request.POST:
        forms = {1: SlideText(request.POST),
                 2: SlideImage(request.POST, request.FILES),
                 3: SlideGraduation(request.POST, request.FILES),
                 4: SlideImageText(request.POST, request.FILES)}

        form = forms.get(int(template_id))

        if form.is_valid():
            pub = Publication()
            pub.user_id = request.user
            pub.tag_id = form.cleaned_data['slide_type']
            pub.type_id = Type.objects.get(pk=1)
            pub.template_id = Template.objects.get(pk=template_id)
            pub.priority_id = Priority.objects.get(pk=1)
            pub.init_date = datetime.combine(form.cleaned_data['start_circulation'],
                                             form.cleaned_data['start_circulation_time'])
            pub.end_date = datetime.combine(form.cleaned_data['end_circulation'],
                                            form.cleaned_data['end_circulation_time'])
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
                image = Image(image=form.cleaned_data.get('image'),
                              number=1,
                              publication_id=pub)
                image.save()

            request.session['draft'] = False
            url = reverse(index) + "?create=1"
            return HttpResponseRedirect(url)

        tag_form = TagCreationForm()
        return render(request, 'DCCNews/slide.html', {'form': form,
                                                      'tagForm': tag_form,
                                                      'image': template.view_prev,
                                                      'new': True,
                                                      'template': template_id})

    if request.session.get('draft', False) and request.GET.get('draft', False):
        template_id = int(request.session.get('template'))
        template = get_object_or_404(Template, pk=template_id)

        initial_data = {'title': request.session.get('title', ""),
                        'subhead': request.session.get('subhead', ""),
                        'body': request.session.get('body', ""),
                        'exhibitor': request.session.get('exhibitor', "asdas"),
                        'date': request.session.get('date', ""),
                        'time': request.session.get('time', ""),
                        'place': request.session.get('place', ""),
                        'start_circulation': request.session.get('start_circulation', ""),
                        'start_circulation_time': request.session.get('start_circulation_time', ""),
                        'end_circulation': request.session.get('end_circulation', ""),
                        'end_circulation_time': request.session.get('end_circulation_time', ""),
                        'slide_type': request.session.get('slide_type', "")}

        forms = {1: SlideText(initial_data),
                 2: SlideImage(initial_data),
                 3: SlideGraduation(initial_data),
                 4: SlideImageText(initial_data)}

        form = forms.get(template_id)
        tag_form = TagCreationForm()
        return render(request, 'DCCNews/slide.html', {'form': form,
                                                      'tagForm': tag_form,
                                                      'image': template.view_prev,
                                                      'new': True,
                                                      'template': template_id})

    forms = {1: SlideText(),
             2: SlideImage(),
             3: SlideGraduation(),
             4: SlideImageText()}
    form = forms.get(int(template_id))
    tag_form = TagCreationForm()
    return render(request, 'DCCNews/slide.html', {'form': form,
                                                  'tagForm': tag_form,
                                                  'image': template.view_prev,
                                                  'new': True,
                                                  'template': template_id})


# edit_slide: vista que cumple los siguientes roles:
# Mostrar el formulario para la edición de una diapositiva almacenada en el sistema
# Si recibe datos por POST, verifica que sean los datos correctos, si no son validos, se vuelve al formulario
# con los mensajes de error correspondietens. Si los datos valiadan, se mantiene en la página de edición y se
# muestra un mensaje de éxito de la operación
@login_required
def edit_slide(request, publication_id):
    pub = get_object_or_404(Publication, pk=publication_id)
    template = get_object_or_404(Template, pk=pub.template_id.id)
    texts = pub.text_set.all()
    images = pub.image_set.all()
    if request.POST:
        forms = {1: SlideText(request.POST),
                 2: SlideImage(request.POST, request.FILES),
                 3: SlideGraduation(request.POST, request.FILES),
                 4: SlideImageText(request.POST, request.FILES)}

        form = forms.get(pub.template_id.id)
        if form.fields.get("image"):
            form.fields["image"].required = False

        if form.is_valid():
            pub.tag_id = form.cleaned_data['slide_type']
            pub.type_id = Type.objects.get(pk=1)
            pub.priority_id = Priority.objects.get(pk=1)
            pub.init_date = datetime.combine(form.cleaned_data['start_circulation'],
                                             form.cleaned_data['start_circulation_time'])
            pub.end_date = datetime.combine(form.cleaned_data['end_circulation'],
                                            form.cleaned_data['end_circulation_time'])
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

            tag_form = TagCreationForm()
            image_name = pub.image_set.filter(number=1).first()
            request.session['draft'] = False
            return render(request, 'DCCNews/slide.html', {'form': form,
                                                          'tagForm': tag_form,
                                                          'image': template.view_prev,
                                                          'image_name': image_name,
                                                          'mensaje': True,
                                                          'template': template.id})

        tag_form = TagCreationForm()
        image_name = pub.image_set.filter(number=1).first()
        return render(request, 'DCCNews/slide.html', {'form': form,
                                                      'tagForm': tag_form,
                                                      'image': template.view_prev,
                                                      'image_name': image_name,
                                                      'template': template.id})

    initial_data = {'title': texts.filter(number=1).first(),
                    'subhead': texts.filter(number=3).first(),
                    'body': texts.filter(number=4).first(),
                    'start_circulation': pub.init_date.strftime('%d-%m-%Y'),
                    'start_circulation_time': pub.init_date.strftime('%H:%M'),
                    'end_circulation': pub.end_date.strftime('%d-%m-%Y'),
                    'end_circulation_time': pub.end_date.strftime('%H:%M'),
                    'slide_type': pub.tag_id.id,
                    'img_url': pub.image_set.filter(number=1).first()}

    image_name = ""
    forms = {1: SlideText(initial_data),
             2: SlideImage(initial_data),
             3: SlideGraduation(initial_data),
             4: SlideImageText(initial_data)}

    form = forms.get(pub.template_id.id)
    if form.fields.get("image"):
        form.fields["image"].required = False
        image_name = pub.image_set.filter(number=1).first()

    tag_form = TagCreationForm()
    return render(request, 'DCCNews/slide.html', {'form': form,
                                                  'tagForm': tag_form,
                                                  'image': template.view_prev,
                                                  'image_name': image_name,
                                                  'template': template.id})


# new_event: vista que cumple los siguientes roles:
# Mostrar el formulario para el ingreso de un nuevo evento a almacenar en el sistema
# Si recibe datos por POST, verifica que sean los datos correctos, si no son validos, se vuelve al formulario
# con los mensajes de error correspondietens. Si los datos valiadan, se vuelve a la página de inicio previo
# almacenamiento de los datos.
@login_required
def new_event(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    if request.POST:
        forms = {5: EventForm(request.POST),
                 6: EventImage(request.POST, request.FILES)}
        form = forms.get(int(template_id))

        if form.is_valid():
            pub = Publication()
            pub.user_id = request.user
            pub.tag_id = form.cleaned_data['slide_type']
            pub.type_id = Type.objects.get(pk=2)
            pub.template_id = Template.objects.get(pk=template_id)
            pub.priority_id = Priority.objects.get(pk=1)
            pub.init_date = datetime.combine(form.cleaned_data['start_circulation'],
                                             form.cleaned_data['start_circulation_time'])
            pub.end_date = datetime.combine(form.cleaned_data['end_circulation'],
                                            form.cleaned_data['end_circulation_time'])
            pub.modification_user_id = request.user

            pub.save()

            text = Text(text=form.cleaned_data['title'],
                        number=1,
                        publication_id=pub)
            text.save()

            if form.cleaned_data.get('exhibitor'):
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

            request.session['draft'] = False
            url = reverse(index) + "?create=1"
            return HttpResponseRedirect(url)

        form.fields['slide_type'].widget = HiddenInput()
        return render(request, 'DCCNews/event.html', {'form': form,
                                                      'image': template.view_prev,
                                                      'new': True,
                                                      "template": template_id})

    if request.session.get('draft', False) and request.GET.get('draft', False):
        template_id = int(request.session.get('template'))
        template = get_object_or_404(Template, pk=template_id)

        initial_data = {'title': request.session.get('title', ""),
                        'subhead': request.session.get('subhead', ""),
                        'body': request.session.get('body', ""),
                        'exhibitor': request.session.get('exhibitor', "asdas"),
                        'date': request.session.get('date', ""),
                        'time': request.session.get('time', ""),
                        'place': request.session.get('place', ""),
                        'start_circulation': request.session.get('start_circulation', ""),
                        'start_circulation_time': request.session.get('start_circulation_time', ""),
                        'end_circulation': request.session.get('end_circulation', ""),
                        'end_circulation_time': request.session.get('end_circulation_time', ""),
                        'slide_type': request.session.get('slide_type', "")}

        forms = {5: EventForm(initial_data),
                 6: EventImage(initial_data)}

        form = forms.get(template_id)
        form.fields['slide_type'].widget = HiddenInput()

        return render(request, 'DCCNews/event.html', {'form': form,
                                                      'image': template.view_prev,
                                                      'new': True,
                                                      'template': template_id})

    forms = {5: EventForm(initial={'slide_type': 3}),
             6: EventImage(initial={'slide_type': 3})}

    form = forms.get(int(template_id))

    form.fields['slide_type'].widget = HiddenInput()
    return render(request, 'DCCNews/event.html', {'form': form,
                                                  'image': template.view_prev,
                                                  'new': True,
                                                  "template": template_id})


# edit_event: vista que cumple los siguientes roles:
# Mostrar el formulario para la edición de un evento almacenado en el sistema
# Si recibe datos por POST, verifica que sean los datos correctos, si no son validos, se vuelve al formulario
# con los mensajes de error correspondietens. Si los datos valiadan, se mantiene en la página de edición y se
# muestra un mensaje de éxito de la operación
@login_required
def edit_event(request, publication_id):
    pub = get_object_or_404(Publication, pk=publication_id)
    template = get_object_or_404(Template, pk=pub.template_id.id)
    texts = pub.text_set.all()
    images = pub.image_set.all()
    if request.POST:
        forms = {5: EventForm(request.POST),
                 6: EventImage(request.POST, request.FILES)}
        form = forms.get(pub.template_id.id)

        if form.fields.get("image"):
            form.fields["image"].required = False

        if form.is_valid():
            pub.tag_id = form.cleaned_data['slide_type']
            pub.type_id = Type.objects.get(pk=2)
            pub.priority_id = Priority.objects.get(pk=1)
            pub.init_date = datetime.combine(form.cleaned_data['start_circulation'],
                                             form.cleaned_data['start_circulation_time'])
            pub.end_date = datetime.combine(form.cleaned_data['end_circulation'],
                                            form.cleaned_data['end_circulation_time'])
            pub.modification_user_id = request.user

            pub.save()
            if form.cleaned_data.get('title'):
                text = texts.filter(number=1).first()
                text.text = form.cleaned_data['title']
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
                #size_images = {6: (170, 170)}

                #size = size_images.get(pub.template_id.id)
                #resize_image(image, size)

            image_name = pub.image_set.filter(number=1).first()

            form.fields['slide_type'].widget = HiddenInput()
            request.session['draft'] = False
            return render(request, 'DCCNews/event.html', {'form': form,
                                                          'image': template.view_prev,
                                                          'image_name': image_name,
                                                          'mensaje': True,
                                                          'template': template.id})

        image_name = pub.image_set.filter(number=1).first()
        form.fields['slide_type'].widget = HiddenInput()
        return render(request, 'DCCNews/event.html', {'form': form,
                                                      'image': template.view_prev,
                                                      'image_name': image_name,
                                                      'template': template.id})

    initial_data = {'title': texts.filter(number=1).first(),
                    'exhibitor': texts.filter(number=2).first(),
                    'date': datetime.strftime(datetime.strptime(str(texts.filter(number=3).first()),
                                                                '%Y-%m-%d'),
                                              '%d-%m-%Y'),
                    'time': time.strftime('%H:%M', time.strptime(str(texts.filter(number=4).first()), "%H:%M:%S")),
                    'place': texts.filter(number=5).first(),
                    'start_circulation': pub.init_date.strftime('%d-%m-%Y'),
                    'start_circulation_time': pub.init_date.strftime('%H:%M'),
                    'end_circulation': pub.end_date.strftime('%d-%m-%Y'),
                    'end_circulation_time': pub.end_date.strftime('%H:%M'),
                    'slide_type': pub.tag_id.id,
                    'img_url': pub.image_set.filter(number=1).first()}

    image_name = ""
    forms = {5: EventForm(initial_data),
             6: EventImage(initial_data)}

    form = forms.get(pub.template_id.id)
    form.fields['slide_type'].widget = HiddenInput()

    if form.fields.get("image"):
        form.fields["image"].required = False
        image_name = pub.image_set.filter(number=1).first()

    return render(request, 'DCCNews/event.html', {'form': form,
                                                  'image': template.view_prev,
                                                  'image_name': image_name,
                                                  'template': template.id})

# save_draft: TODO
def save_draft(request, template_id):
    if request.POST:
        forms = {1: SlideText(request.POST),
                 2: SlideImage(request.POST),
                 3: SlideGraduation(request.POST),
                 4: SlideImageText(request.POST),
                 5: EventForm(request.POST),
                 6: EventImage(request.POST)}

        form = forms.get(int(template_id))
        form.is_valid()
        keys_to_delete = ['title', 'subhead', 'body', 'exhibitor', 'date', 'time', 'place', 'start_circulation',
                          'start_circulation_time', 'end_circulation', ' end_circulation_time', 'template', 'draft']

        for key in keys_to_delete:
            if key in request.session.keys():
                del request.session[key]

        request.session['title'] = form.cleaned_data.get('title', "")
        request.session['subhead'] = form.cleaned_data.get('subhead', "")
        request.session['body'] = form.cleaned_data.get('body', "")
        request.session['exhibitor'] = form.cleaned_data.get('exhibitor', "")

        date = form.cleaned_data.get('date', datetime.today())
        request.session['date'] = date.strftime('%d-%m-%Y')

        time_event = form.cleaned_data.get('time', datetime.today())
        request.session['time'] = time_event.strftime('%H:%M')

        request.session['place'] = form.cleaned_data.get('place', "")

        start_circulation = form.cleaned_data.get('start_circulation', datetime.today())
        request.session['start_circulation'] = start_circulation.strftime('%d-%m-%Y')

        start_circulation_time = form.cleaned_data.get('start_circulation_time', datetime.today())
        request.session['start_circulation_time'] = start_circulation_time.strftime('%H:%M')

        end_circulation = form.cleaned_data.get('end_circulation', datetime.today())
        request.session['end_circulation'] = end_circulation.strftime('%d-%m-%Y')

        end_circulation_time = form.cleaned_data.get('end_circulation_time', datetime.today() + timedelta(hours=1))
        request.session['end_circulation_time'] = end_circulation_time.strftime('%H:%M')

        slide_type = form.cleaned_data.get('slide_type', "")
        request.session['slide_type'] = slide_type.id if slide_type != "" else ""

        request.session['template'] = template_id
        request.session['draft'] = True

        return HttpResponse(status=200)


# load_draft: TODO
def load_draft(request):
    if request.session.get('draft', False):
        template_id = int(request.session.get('template'))
        slide_forms= [1, 2, 3, 4]
        event_forms = [5, 6]
        if template_id in slide_forms:
            url = reverse(new_slide, kwargs={'template_id': template_id}) + "?draft=1"
            return HttpResponseRedirect(url)

        if template_id in event_forms:
            url = reverse(new_event, kwargs={'template_id': template_id}) + "?draft=1"
            return HttpResponseRedirect(url)

    url = reverse(index)
    return HttpResponseRedirect(url)


# Busca una diapositiva: Dado un formulario busca todos las diapositivas
# en la base de datos que cumplan con las condiciones, puede recibir 
# a traves de un formulario el titulo y el tipo de la diapositiva
# a demas controla a traves del mismo formulario si se va a borrar un
# elemnto, se uso un boton de submit para borrar, para no perder los datos
# de la busqueda, se uso la misma idea para el paginator
# 
@login_required
def search_slide(request):
    #crea las variables
    max = 15
    toShow = []
    empty = False
    newSearch = True
    Borrado = False
    failFoundBorrar = False
    
    if request.POST and 'delete' in request.POST:
        # Si se pidio borrar se busca el evento en la base de datos
        if(Publication.objects.filter(id=request.POST.get('delete')).exists()):
             # si existe se borra
             toDelete = Publication.objects.get(id=request.POST.get('delete'))
             toDelete.delete()
             Borrado = True
        else:
            #Si no existe se envia un mensaje de error
            failFoundBorrar = True
    
    #Prepara la consulta a la base de datos
    Pubs = Publication.objects.order_by('-creation_date').filter(type_id__name__icontains="slide")
    # if this is a POST request we need to process the form data
    if request.POST:
        # create a form instance and populate it with data from the request:
        form = SearchSlide(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if form.cleaned_data.get('titulo'):
                # si tiene titulo, busca por el titulo
                newSearch = False
                titulo = form.cleaned_data['titulo']
                Pubs = Pubs.filter(text__number__exact=1, text__text__icontains=titulo)
            # print(slide_type)
            if form.cleaned_data.get('slide_type'):
                # si tiene tipo de diapositiva, busca por el tipo de diapositiva
                newSearch = False
                slide_type = form.cleaned_data['slide_type']
                Pubs = Pubs.filter(tag_id__name__icontains=slide_type)
    # Notar que la busqueda se hace por cada input uno sobre el otro
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchSlide()
        newSearch = True
        # si es una busqueda nueva, crea el formulario

    # --- busqueda
    for pub in Pubs:
        #    print(pub)
        texts = pub.text_set.all()
        title = texts.filter(number__exact=1).first()
        if title == None:
            title = "IMAGEN"
        p = {"title": title,
             "type": pub.tag_id.name,
             "id": pub.pk,
             }
        toShow.append(p)
        # print(p.get("title"))

    if not toShow:
        empty = True

    paginator = Paginator(toShow, max)
    toShowl = paginator.page(1)
    #Si el "boton" que se apreto era de cambio de pagina, se guarda el numero y se cambia de pagina
    if request.POST and 'p' in request.POST:
        page = request.POST.get('p')
        try:
            toShowl = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            toShowl = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            toShowl = paginator.page(paginator.num_pages)

    cancel = False
    if request.GET.get('cancel') and not request.POST :
        cancel = True

    return render(request, 'DCCNews/template_search.html',
                  {"toShowl": toShowl, "form": form, "empty": empty, "newSearch": newSearch, "cancel": cancel, "Borrado": Borrado, "failFoundBorrar":failFoundBorrar})


# Busca una evento: Dado un formulario busca todos los eventos
# en la base de datos que cumplan con las condiciones, puede recibir 
# a traves de un formulario el titulo o el expositor o la fecha
# a demas controla a traves del mismo formulario si se va a borrar un
# elemnto, se uso un boton de submit para borrar, para no perder los datos
# de la busqueda, se uso la misma idea para el paginator
# 
@login_required
def search_event(request):
    #crea las variables
    max = 15
    toShow = []
    cancel = False
    empty = False
    newSearch = True
    Borrado = False
    failFoundBorrar = False
    if request.POST and 'delete' in request.POST:
        # Si se pidio borrar se busca el evento en la base de datos
        if(Publication.objects.filter(id=request.POST.get('delete')).exists()):
            # si existe se borra
             toDelete = Publication.objects.get(id=request.POST.get('delete'))
             toDelete.delete()
             Borrado = True
        else:
            #Si no existe se envia un mensaje de error
            failFoundBorrar = True
    #Prepara la consulta a la base de datos
    Pubs = Publication.objects.order_by('-creation_date').filter(type_id__name__icontains="event")
    #If this is a POST request we need to process the form data
    if request.POST:
        # create a form instance and populate it with data from the request:
        form = SearchEvent(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if form.cleaned_data.get('titulo'):
                # si tiene titulo, busca por el titulo
                newSearch = False
                titulo = form.cleaned_data['titulo']
                # print titulo
                Pubs = Pubs.filter(text__number__exact=1, text__text__icontains=titulo)
            # print(expositor)
            if form.cleaned_data.get('expositor'):
                #si tiene expositor busca por expositor
                newSearch = False
                expositor = form.cleaned_data['expositor']
                Pubs = Pubs.filter(text__number__exact=2, text__text__icontains=expositor)
                # print(date)
            if form.cleaned_data.get('date'):
                # si tiene fecha busca tambien por fecha
                newSearch = False
                date = form.cleaned_data['date']
                Pubs = Pubs.filter(text__number__exact=3, text__text__icontains=date)
    # Notar que la busqueda se hace por cada input uno sobre el otro
    else:
        # si es una busqueda nueva, crea el formulario
        form = SearchEvent()
        newSearch = True

    # Dado que las publicaciones tienen texto e imagenes, se tiene que buscar cada una de ellas
    for pub in Pubs:
        texts = pub.text_set.all()
        expositor = texts.filter(number__exact=2).first()
        p = {"title": texts.filter(number__exact=1).first(),
             "expositor": expositor,
             "id": pub.pk,
             }
        # print(p.get("title"))
        toShow.append(p)

    if not toShow:
        # Si el dicionario con resultados esta vacio, se setea la variable empty true
        empty = True
    # Se genera un paginator
    paginator = Paginator(toShow, max)
    # se pone el la primera pagina
    toShowl = paginator.page(1)
    
    #Si el "boton" que se apreto era de cambio de pagina, se guarda el numero y se cambia de pagina
    if request.POST and 'p' in request.POST:
        page = request.POST.get('p')
        try:
            toShowl = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            toShowl = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            toShowl = paginator.page(paginator.num_pages)

    if request.GET.get('cancel'):
        cancel = True

    return render(request, 'DCCNews/template_search_evento.html',
                  {"toShowl": toShowl, "form": form, "empty": empty, "newSearch": newSearch, 'cancel': cancel, "Borrado": Borrado, "failFoundBorrar": failFoundBorrar})

# visualize: LLama a la visualizacion y previsualización. Esto depende si el llamado se hace con get o con post
# Si se llama con post, se recibe una serie de parametros que hace conforman una noticia o un evento y lo muestra
# Si se llama con get, se filtran todas las noticias y eventos que deben mostrarse y se muestra el display haciendo
# un loop sobre las noticias
def visualize(request, template_id=None):
    event_list = []
    slide_list = []
    preview = True
    if request.POST:
        if template_id == "1":
            form = SlideText(request.POST)
            if form.is_valid():
                template = Template.objects.get(pk=template_id)
                title = form.cleaned_data['title']
                text = form.cleaned_data['body']
                tag = form.cleaned_data['slide_type']
                p = {"id": 1,
                     "title": title,
                     "text": text,
                     "template": template.view,
                     "tag": tag
                     }
                slide_list.append(p)

        elif template_id == "2":
            form = SlideImage(request.POST, request.FILES)
            if form.is_valid():
                template = Template.objects.get(pk=template_id)
                image = Temp(image=request.FILES['image'])
                image.save()
                tag = form.cleaned_data['slide_type']
                p = {"id":1,
                     "image": image.image,
                     "template": template.view,
                     "tag": tag,
                     }
                slide_list.append(p)
            else:
                template = Template.objects.get(pk=template_id)
                image = form.cleaned_data['img_url']
                tag = form.cleaned_data['slide_type']
                p = {"id":1,
                     "image": "images/"+image,
                     "template": template.view,
                     "tag": tag,
                     }
                slide_list.append(p)

        elif template_id == "3":
            form = SlideGraduation(request.POST, request.FILES)
            if form.is_valid():
                template = Template.objects.get(pk=template_id)
                title = form.cleaned_data['title']
                subhead = form.cleaned_data['subhead']
                image = Temp(image=request.FILES['image'])
                image.save()
                tag = form.cleaned_data['slide_type']
                p = {"id": 1,
                     "title": title,
                     "subhead": subhead,
                     "image": image.image,
                     "template": template.view,
                     "tag": tag
                     }
                slide_list.append(p)
            else:
                template = Template.objects.get(pk=template_id)
                title = form.cleaned_data['title']
                subhead = form.cleaned_data['subhead']
                image = form.cleaned_data['img_url']
                tag = form.cleaned_data['slide_type']
                p = {"id": 1,
                     "title": title,
                     "subhead": subhead,
                     "image": "images/"+image,
                     "template": template.view,
                     "tag": tag
                     }
                slide_list.append(p)

        elif template_id == "4":
            form = SlideImageText(request.POST, request.FILES)
            if form.is_valid():
                template = Template.objects.get(pk=template_id)
                title = form.cleaned_data['title']
                text = form.cleaned_data['body']
                tag = form.cleaned_data['slide_type']
                image = Temp(image=request.FILES['image'])
                image.save()
                p = {"id": 1,
                     "title": title,
                     "text": text,
                     "image": image.image,
                     "template": template.view,
                     "tag": tag,
                     }
                slide_list.append(p)
            else:
                template = Template.objects.get(pk=template_id)
                title = form.cleaned_data['title']
                text = form.cleaned_data['body']
                tag = form.cleaned_data['slide_type']
                image = form.cleaned_data['img_url']
                p = {"id":1,
                    "title": title,
                     "text": text,
                     "image": "images/"+image,
                     "template": template.view,
                     "tag": tag,
                     }
                slide_list.append(p)

        elif template_id == "5":
            form = EventForm(request.POST)
            if form.is_valid():
                template = Template.objects.get(pk=template_id)
                title = form.cleaned_data['title']
                exhibitor = form.cleaned_data['exhibitor']
                date = form.cleaned_data['date']
                time = form.cleaned_data['time']
                place = form.cleaned_data['place']
                p = {"title": title,
                     "exhibitor": exhibitor,
                     "date": date,
                     "time": time,
                     "place": place,
                     "template": template.view,
                     }
                event_list.append(p)

        elif template_id == "6":
            form = EventImage(request.POST, request.FILES)
            if form.is_valid():
                template = Template.objects.get(pk=template_id)
                title = form.cleaned_data['title']
                exhibitor = form.cleaned_data['exhibitor']
                date = form.cleaned_data['date']
                time = form.cleaned_data['time']
                place = form.cleaned_data['place']
                image = Temp(image=request.FILES['image'])
                image.save()
                p = {"title": title,
                     "exhibitor": exhibitor,
                     "date": date,
                     "time": time,
                     "place": place,
                     "image": image.image,
                     "template": template.view,
                     }
                event_list.append(p)
            else:
                template = Template.objects.get(pk=template_id)
                title = form.cleaned_data['title']
                exhibitor = form.cleaned_data['exhibitor']
                date = form.cleaned_data['date']
                time = form.cleaned_data['time']
                place = form.cleaned_data['place']
                image = form.cleaned_data['img_url']
                p = {"title": title,
                     "exhibitor": exhibitor,
                     "date": date,
                     "time": time,
                     "place": place,
                     "image": "images/"+image,
                     "template": template.view,
                     }
                event_list.append(p)

    else:
        preview = False
        slides = Publication.objects.order_by('-creation_date')\
            .filter(type_id__name__icontains="slide")\
            .filter(init_date__lte=datetime.today())\
            .filter(end_date__gte=datetime.today())
        events = Publication.objects.order_by('end_date')\
            .filter(type_id__name__icontains="event")\
            .filter(init_date__lte=datetime.today())\
            .filter(end_date__gte=datetime.today())[:3]
        for slide in slides:
            texts = slide.text_set.all()
            images = slide.image_set.all()
            template = slide.template_id
            tag = slide.tag_id
            p = {}
            if template.name == "Noticias":
                p = {"id": slide.id,
                     "title": texts.get(number=1),
                     "text": texts.get(number=4),
                     "template": template.view,
                     "tag": tag.name,
                     }
            elif template.name == "Afiche":
                p = {"id": slide.id,
                     "image": images.first().image,
                     "template": template.view,
                     "tag": tag.name,
                     }
            elif template.name == "Titulaciones":
                p = {"id": slide.id,
                     "title": texts.get(number=1),
                     "subhead": texts.get(number = 3),
                     "image": images.first().image,
                     "template": template.view,
                     "tag": tag.name,
                     }
            elif template.name == "NoticiaImagen":
                p = {"id": slide.id,
                     "title": texts.get(number=1),
                     "text": texts.get(number=4),
                     "image": images.first().image,
                     "template": template.view,
                     "tag": tag.name,
                    }
            slide_list.append(p)

        for event in events:
            texts = event.text_set.all()
            images = event.image_set.all()
            template = event.template_id
            if template.name == "Evento":
                p = {"title": texts.get(number=1),
                     "exhibitor": texts.filter(number=2).first(),
                     "date": datetime.strptime(str(texts.get(number=3)), "%Y-%m-%d"),
                     "time": datetime.strptime(str(texts.get(number=4)), "%H:%M:%S"),
                     "place": texts.get(number=5),
                     "template": template.view,
                     }
            elif template.name == "EventoImagen":
                p = {"title": texts.get(number=1),
                     "exhibitor": texts.filter(number=2).first(),
                     "date": datetime.strptime(str(texts.get(number=3)), "%Y-%m-%d"),
                     "time": datetime.strptime(str(texts.get(number=4)), "%H:%M:%S"),
                     "place": texts.get(number=5),
                     "image": images.first().image,
                     "template": template.view,
                     }
            event_list.append(p)

    return render(request, 'DCCNews/visualization.html', {"slide_list": slide_list, "event_list": event_list, "preview":preview})

# update_news: practicamente lo mismo que visualize, pero usado para la petición ajax que se usa para actualizar
# las lista de noticias y de eventos
def update_news(request):
    event_list = []
    slide_list = []
    slides = Publication.objects.order_by('-creation_date') \
        .filter(type_id__name__icontains="slide") \
        .filter(init_date__lte=datetime.today()) \
        .filter(end_date__gte=datetime.today())
    events = Publication.objects.order_by('end_date') \
                 .filter(type_id__name__icontains="event") \
                 .filter(init_date__lte=datetime.today()) \
                 .filter(end_date__gte=datetime.today())[:3]
    for slide in slides:
        texts = slide.text_set.all()
        images = slide.image_set.all()
        template = slide.template_id
        tag = slide.tag_id
        p = {}
        if template.name == "Noticias":
            p = {"id": slide.id,
                 "title": texts.get(number=1),
                 "text": texts.get(number=4),
                 "template": template.view,
                 "tag": tag.name,
                 }
        elif template.name == "Afiche":
            p = {"id": slide.id,
                 "image": images.first().image,
                 "template": template.view,
                 "tag": tag.name,
                 }
        elif template.name == "Titulaciones":
            p = {"id": slide.id,
                 "title": texts.get(number=1),
                 "subhead": texts.get(number = 3),
                 "image": images.first().image,
                 "template": template.view,
                 "tag": tag.name,
                 }
        elif template.name == "NoticiaImagen":
            p = {"id": slide.id,
                 "title": texts.get(number=1),
                 "text": texts.get(number=4),
                 "image": images.first().image,
                 "template": template.view,
                 "tag": tag.name,
                 }
        slide_list.append(p)

    for event in events:
        texts = event.text_set.all()
        images = event.image_set.all()
        template = event.template_id
        if template.name == "Evento":
            p = {"title": texts.get(number=1),
                 "exhibitor": texts.filter(number=2).first(),
                 "date": datetime.strptime(str(texts.get(number=3)), "%Y-%m-%d"),
                 "time": datetime.strptime(str(texts.get(number=4)), "%H:%M:%S"),
                 "place": texts.get(number=5),
                 "template": template.view,
                 }
        elif template.name == "EventoImagen":
            p = {"title": texts.get(number=1),
                 "exhibitor": texts.filter(number=2).first(),
                 "date": datetime.strptime(str(texts.get(number=3)), "%Y-%m-%d"),
                 "time": datetime.strptime(str(texts.get(number=4)), "%H:%M:%S"),
                 "place": texts.get(number=5),
                 "image": images.first().image,
                 "template": template.view,
                 }
        event_list.append(p)

    return render(request, 'DCCNews/news.html', {"slide_list": slide_list, "event_list": event_list})
