__author__ = 'milenkotomic'
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, DateInput, NumberInput


class MyDateInput(forms.DateInput):
    input_type = 'datetime-local'


# Formulario para inicio de sesión
class LoginForm(Form):
    user = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Usuario',
                                                                        'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña',
                                                                                'class': 'form-control'}))


class SlideForm(Form):
    CHOICES = (('0', 'Seleccionar tipo'),
               ('1', 'Curso Nuevo'),
               ('2', 'Charla'))

    title = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Título')

    subhead = forms.CharField(required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control'}),
                              label='Bajada de título')

    start_circulation = forms.DateTimeField(required=True,
                                            widget=MyDateInput(attrs={'class': 'form-control'}),
                                            label='Inicio de Circulación')

    end_circulation = forms.DateTimeField(required=True,
                                          widget=MyDateInput(attrs={'class': 'form-control'}),
                                          label='Inicio de Circulación')

    slide_type = forms.ChoiceField(required=True,
                                   choices=CHOICES,
                                   widget=forms.Select(attrs={'class': 'form-control'}),
                                   label='Tipo de Diapositiva')


class SlideText(SlideForm):
    body = forms.CharField(required=True,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'rows':4,
                                                        'cols': 40}),
                           label='Cuerpo de la diapositiva')

    image = forms.ImageField(required=True,
                             widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                             label='Imagen')


class SlideImage(SlideForm):
    image = forms.ImageField(required=True,
                             widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                             label='Imagen')