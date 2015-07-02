# -*- coding: utf-8 -*-
from DCCNews.models import Tag

__author__ = 'milenkotomic'


from django import forms
from django.forms import Form, ModelForm


class MyDateTimeInput(forms.DateInput):
    input_type = 'datetime-local'


class MyTimeInput(forms.DateInput):
    input_type = 'time'


class MyDateInput(forms.DateInput):
    input_type = 'date'

#class myCountTextArea(forms.CharField):
    

# Formulario para inicio de sesión
class LoginForm(Form):
    user = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Usuario',
                                                                        'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña',
                                                                                'class': 'form-control'}))


class TagCreationForm(Form):
    new_tag = forms.CharField(max_length=11,
                              required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'display': 'block'}),
                              label='Ingrese tag')


class PublicationForm(Form):
    start_circulation = forms.DateField(required=True,
                                        widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'DD-MM-AAAA',
                                                                      'onChange': 'checkCirculation()'}),
                                        label='Inicio de Circulación',
                                        input_formats=['%d-%m-%Y',
                                                       '%Y-%m-%d'])

    start_circulation_time = forms.TimeField(required=True,
                                             widget=MyTimeInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'HH:MM',
                                                                       'onChange': 'checkCirculation()',
                                                                       'onfocus': 'defaultTime(this)'}),
                                             label='Inicio de Circulación',
                                             input_formats=['%H:%M'])

    end_circulation = forms.DateField(required=True,
                                      widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'DD-MM-AAAA',
                                                                    'onChange': 'checkCirculation()'}),
                                      label='Fin de Circulación',
                                      input_formats=['%d-%m-%Y',
                                                     '%Y-%m-%d'])

    end_circulation_time = forms.TimeField(required=True,
                                           widget=MyTimeInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'HH:MM',
                                                                     'onChange': 'checkCirculation()',
                                                                     'onfocus': 'defaultTime(this)'}),
                                           label='Fin de Circulación',
                                           input_formats=['%H:%M'])

    slide_type = forms.ModelChoiceField(required=True,
                                        queryset=Tag.objects.all().order_by('name'),
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        label='Tipo de Diapositiva')

    img_url = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'style': 'display: none'}),
                            label='Imagen existente')

    def clean(self):
        cleaned_data = super(PublicationForm, self).clean()
        start_circulation = cleaned_data.get("start_circulation")
        end_circulation = cleaned_data.get("end_circulation")
        start_circulation_time = cleaned_data.get("start_circulation_time")
        end_circulation_time = cleaned_data.get("end_circulation_time")

        if start_circulation:
            if start_circulation.year < 1900:
                msg = 'Fecha inválida'
                self.add_error('start_circulation', msg)

        if end_circulation:
            if end_circulation.year < 1900:
                msg = 'Fecha inválida'
                self.add_error('end_circulation', msg)

        start_circulation = cleaned_data.get("start_circulation")
        end_circulation = cleaned_data.get("end_circulation")

        if start_circulation and end_circulation and start_circulation_time and end_circulation_time:
            if (start_circulation > end_circulation) or \
                    (start_circulation == end_circulation and start_circulation_time >= end_circulation_time):
                msg = 'La fecha de término debe ser posterior a la fecha de inicio'
                self.add_error('start_circulation', msg)
                del self.cleaned_data['end_circulation']


class SlideText(PublicationForm):
    title = forms.CharField(max_length=65,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Título')

    body = forms.CharField(max_length=1000,
                           required=True,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'rows': 4,
                                                        'cols': 40}),
                           label='Cuerpo de la diapositiva')


class SlideImage(PublicationForm):
    title = forms.CharField(max_length=65,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Título')

    image = forms.ImageField(required=True,
                             widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                             label='Imagen')


class SlideGraduation(PublicationForm):
    title = forms.CharField(max_length=65,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Título')

    subhead = forms.CharField(max_length=100,
                              required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control'}),
                              label='Bajada de Título')

    image = forms.ImageField(required=True,
                             widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                             label='Imagen')


class SlideImageText(PublicationForm):
    title = forms.CharField(max_length=65,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Título')

    body = forms.CharField(max_length=1000,
                           required=True,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'rows': 4,
                                                        'cols': 40}),
                           label='Cuerpo de la diapositiva')

    image = forms.ImageField(required=True,
                             widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                             label='Imagen')


class EventForm(PublicationForm):
    title = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Título')

    exhibitor = forms.CharField(max_length=100,
                                required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label='Expositor')

    date = forms.DateField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'DD-MM-AAAA'}),
                           label='Fecha',
                           input_formats=['%d-%m-%Y',
                                          '%Y-%m-%d'])

    time = forms.TimeField(required=True,
                           widget=MyTimeInput(attrs={'class': 'form-control',
                                                     'placeholder': 'HH:MM',
                                                     'onfocus': 'defaultTime(this)'}),
                           label='Hora',
                           input_formats=['%H:%M'])

    place = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Lugar')


class EventImage(EventForm):
    image = forms.ImageField(required=True,
                             widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                             label='Imagen')


class TagForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label='Nombre')

    class Meta:
        model = Tag
        fields = ['name']


#El formulario padre, en particular el titulo para busqueda
class SearchElement(Form):
    #input del titulo
    titulo = forms.CharField(required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             label='Búsqueda por título:')

    def clean_titulo(self):
        #borra los espacios al principio y al final
        return self.cleaned_data['titulo'].strip()


#El formulario para busquedas de diapositivas
class SearchSlide(SearchElement):
    # se agrega el tipo de diapositiva
    slide_type = forms.ModelChoiceField(required=False,
                                        queryset=Tag.objects.all().order_by('name'),
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        label='Búsqueda por tipo:')


#El formulario de busqueda de eventos
class SearchEvent(SearchElement):
    #se agrega el input para buscar el expositor
    expositor = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label='Búsqueda por expositor:')
    #se agrega el input para las fecha
    date = forms.DateField(required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'DD-MM-AAAA'}),
                           label='Búsqueda por fecha:',
                           input_formats=['%d-%m-%Y',
                                          '%Y-%m-%d'])

    def clean_expositor(self):
        return self.cleaned_data['expositor'].strip()
