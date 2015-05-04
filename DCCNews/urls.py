from NoticiasDCC import settings

__author__ = 'milenkotomic'
from django.conf.urls import patterns, include, url
from DCCNews import views

urlpatterns = patterns('',
                       url(r'^login/', views.login_view, name='login'),
                       url(r'^logout/', views.logout_view, name='logout'),
                       url(r'^index/', views.index, name='index'),
                       url(r'^publication/new/template', views.select_template, name='template_selection'),
                       url(r'^slide/new/(?P<template_id>\d+)', views.new_slide, name='new_slide'),
                       url(r'^slide/edit/(?P<publicaction_id>\d+)/', views.edit_slide, name='edit_slide'),
                       url(r'^event/new/(?P<template_id>\d+)', views.new_event, name='new_event'),
                       url(r'^event/edit/(?P<publicaction_id>\d+)/', views.edit_event, name='edit_event'),

                       url(r'^$', views.index, name='index'),
                       url(r'^search/', views.search_contenido, name='search_contenido'),
                       url(r'^search_evento/', views.search_contenido_evento, name='search_contenido_evento'),
                       )


if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT}))