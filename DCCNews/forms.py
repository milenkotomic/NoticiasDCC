__author__ = 'milenkotomic'
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, DateInput, NumberInput


# Formulario para inicio de sesión
class LoginForm(Form):
    user = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Usuario',
                                                                        'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña',
                                                                                'class': 'form-control'}))
