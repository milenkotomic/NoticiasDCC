__author__ = 'milenkotomic'
from django.conf.urls import patterns, include, url
from DCCNews import views

urlpatterns = patterns('',
                       url(r'^login/', views.login_view, name='login'),
                       url(r'^logout/', views.logout_view, name='logout'),
                       url(r'^index/', views.index, name='index'),

                       url(r'^$', views.index, name='index'),
                       )

