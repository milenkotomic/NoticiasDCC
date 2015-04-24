__author__ = 'milenkotomic'
from django.conf.urls import patterns, include, url
from DCCNews import views

urlpatterns = patterns('',
                       url(r'^login/', views.login_view, name='login'),
                       url(r'^logout/', views.logout_view, name='logout'),
                       url(r'^index/', views.index, name='index'),
                       url(r'^publication/new/(?P<template_id>\d+)', views.new_publication, name='new_publication'),
                       url(r'^publication/edit/(?P<publicaction_id>\d+)/', views.edit_publication, name='edit_publication'),

                       url(r'^$', views.index, name='index'),
                       url(r'^search/', views.search_contenido, name='search_contenido'),
                       url(r'^search_evento/', views.search_contenido_evento, name='search_contenido_evento'),
                       )

