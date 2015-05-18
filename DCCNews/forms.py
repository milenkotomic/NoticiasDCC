# -*- coding: utf-8 -*-
from DCCNews.models import Tag

__author__ = 'milenkotomic'


from django import forms
from django.forms import Form


class MyDateTimeInput(forms.DateInput):
    input_type = 'datetime-local'


class MyTimeInput(forms.DateInput):
    input_type = 'time'


class MyDateInput(forms.DateInput):
    input_type = 'date'


# Formulario para inicio de sesión
class LoginForm(Form):
    user = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Usuario',
                                                                        'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña',
                                                                                'class': 'form-control'}))


class PublicationForm(Form):
    start_circulation = forms.DateField(required=True,
                                        widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'DD-MM-AAAA',
                                                                      'onChange': 'checkCirculation()'}),
                                        label='Inicio de Circulación',
                                        input_formats=['%d-%m-%Y',
                                                       '%Y-%m-%d'])

    start_circulation_time = forms.TimeField(required=True,
                                             widget=forms.TimeInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'HH:MM',
                                                                           'onChange': 'checkCirculation()'}),
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
                                           widget=forms.TimeInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'HH:MM',
                                                                         'onChange': 'checkCirculation()'}),
                                           label='Fin de Circulación',
                                           input_formats=['%H:%M'])

    slide_type = forms.ModelChoiceField(required=True,
                                        queryset=Tag.objects.all().order_by('name'),
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        label='Tipo de Diapositiva')

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
            if (start_circulation > end_circulation) or (start_circulation == end_circulation and start_circulation_time >= end_circulation_time):
                msg = 'La fecha de término debe ser posterior a la fecha de inicio'
                self.add_error('start_circulation', msg)
                del self.cleaned_data['end_circulation']


class SlideText(PublicationForm):
    title = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Título')

    body = forms.CharField(required=True,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'rows': 4,
                                                        'cols': 40}),
                           label='Cuerpo de la diapositiva')


class SlideImage(PublicationForm):
    title = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Título')

    image = forms.ImageField(required=True,
                             widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                             label='Imagen')


class EventForm(PublicationForm):
    title = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Título')

    exhibitor = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label='Expositor')

    date = forms.DateField(required=True,
                           widget=MyDateInput(attrs={'class': 'form-control',
                                                     'placeholder': 'DD-MM-AAAA'}),
                           label='Fecha',
                           input_formats=['%d-%m-%Y',
                                          '%Y-%m-%d'])

    time = forms.TimeField(required=True,
                           widget=MyTimeInput(attrs={'class': 'form-control',
                                                     'placeholder': 'HH:MM'}),
                           label='Hora')

    place = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Lugar')


class EventImage(EventForm):
    image = forms.ImageField(required=True,
                             widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                             label='Imagen')

class SearchSlide(Form):
    #testing
    titulo = forms.CharField(required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             label='Busqueda por titulo')
    #diferenciar tag de eventos y diapositivas
    slide_type = forms.ModelChoiceField(required=False,
                                        queryset=Tag.objects.all().order_by('name'),
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        label='Busqueda por tipo')
class SearchEvent(SearchSlide):
    expositor = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label='Busqueda por expositor')
    date = forms.DateField(required=False,
                           widget=MyDateInput(attrs={'class': 'form-control'}),
                           label='Busqueda por fecha',
                           input_formats=['%d-%m-%Y',
                                          '%Y-%m-%d'])
