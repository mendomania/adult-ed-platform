# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
from django.contrib import admin

app_name = 'osr'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'offerings/$', views.OfferingsView.as_view(), name='offerings'),
    url(r'results/$', views.ResultsView.as_view(), name='results'),
    url(r'widget/$', views.WidgetView.as_view(), name='widget'),
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^chaining/', include('smart_selects.urls')),
]