from NoticiasDCC import settings

__author__ = 'milenkotomic'
from django.conf.urls import patterns, url
from DCCNews import views

urlpatterns = patterns('',
                       url(r'^login/', views.login_view, name='login'),
                       url(r'^logout/', views.logout_view, name='logout'),
                       url(r'^index/', views.index, name='index'),
                       url(r'^publication/new/template', views.select_template, name='template_selection'),
                       url(r'^slide/new/(?P<template_id>\d+)', views.new_slide, name='new_slide'),
                       url(r'^slide/edit/(?P<publication_id>\d+)/', views.edit_slide, name='edit_slide'),
                       url(r'^event/new/(?P<template_id>\d+)', views.new_event, name='new_event'),
                       url(r'^event/edit/(?P<publication_id>\d+)/', views.edit_event, name='edit_event'),
                       url(r'^createtag/', views.create_tag, name='createTag'),
                       url(r'^deletetag/', views.delete_tag, name='deleteTag'),
                       url(r'^savedraft/(?P<template_id>\d+)/', views.save_draft, name='save_draft'),
                       url(r'^loaddraft/', views.load_draft, name='load_draft'),

                       url(r'^$', views.index, name='index'),
                       url(r'^search/slide/', views.search_slide, name='search_slide'),#pagina de busqueda de diapositivas
                       url(r'^search/event/', views.search_event, name='search_event'),#pagina de busqueda de eventos
                       url(r'^visualize/(?P<template_id>\d+)', views.visualize, name='visualize_content'),
                       url(r'^update/', views.update_news, name='update_content'),
                       )
