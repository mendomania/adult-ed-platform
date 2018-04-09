# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'osr'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'offerings/$', views.OfferingsView.as_view(), name='offerings'),
    #url(r'offerings/$', views.get_offerings, name='offerings'),
    #url(r'^search/$', views.search, name='search'),
]