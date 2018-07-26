# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    url(r'^osr/', include('osr.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^i18n/',include('django.conf.urls.i18n'))
]
