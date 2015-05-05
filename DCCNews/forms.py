# -*- coding: utf-8 -*-
from DCCNews.models import Tag

__author__ = 'milenkotomic'


from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, DateInput, NumberInput


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
    start_circulation = forms.DateTimeField(required=True,
                                            widget=MyDateTimeInput(attrs={'class': 'form-control'}),
                                            label='Inicio de Circulación',
                                            input_formats=['%d-%m-%YT%H:%M',
                                                           '%Y-%m-%dT%H:%M'])

    end_circulation = forms.DateTimeField(required=True,
                                          widget=MyDateTimeInput(attrs={'class': 'form-control'}),
                                          label='Fin de Circulación',
                                          input_formats=['%d-%m-%YT%H:%M',
                                                         '%Y-%m-%dT%H:%M'])

    slide_type = forms.ModelChoiceField(required=True,
                                        queryset=Tag.objects.all().order_by('name'),
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        label='Tipo de Diapositiva')


class SlideText(PublicationForm):
    title = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Título')

    body = forms.CharField(required=True,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'rows':4,
                                                        'cols': 40}),
                           label='Cuerpo de la diapositiva')


class SlideImage(PublicationForm):
    image = forms.ImageField(required=True,
                             widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                             label='Imagen')


class EventForm(PublicationForm):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label='Nombre')

    exhibitor = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label='Expositor')

    date = forms.DateField(required=True,
                           widget=MyDateInput(attrs={'class': 'form-control'}),
                           label='Fecha',
                           input_formats=['%d-%m-%Y',
                                          '%Y-%m-%d'])

    time = forms.TimeField(required=True,
                           widget=MyTimeInput(attrs={'class': 'form-control'}),
                           label='Hora')

    place = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label='Lugar')


class EventImage(EventForm):
    image = forms.ImageField(required=True,
                             widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                             label='Imagen')
