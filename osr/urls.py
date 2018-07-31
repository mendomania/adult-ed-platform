# -*- coding: utf-8 -*-
from . import views
from django.conf.urls import url

app_name = 'osr'
urlpatterns = [  

    # Static landing page
    url(r'intro/$', views.intro, name='intro'),
    # Matchmaker page
    url(r'matchmaker/$', views.matchmaker, name='matchmaker'),
    # Static glossary page
    url(r'dictionary/$', views.dictionary, name='dictionary'),   
    # Static feedback page
    url(r'feedback/$', views.feedback, name='feedback'),        

    # Results page
    url(r'transition/$', views.transition, name='transition'),
    # Comparison page
    url(r'comparison/$', views.comparison, name='comparison'),

    # Dynamic program pages
    # ex: /program/adc/
    url(r'program/(?P<program_code>[a-z]+)/$', views.detail_program, name='detail_program'),
    # Print functionality
    url(r'print/$', views.ResultsPDFView.as_view(), name='print'),
    # Email functionality
    url(r'email/$', views.email, name='email'),

    # Deprecated: Dynamic offering page
    url(r'offerings/$', views.OfferingsView.as_view(), name='offerings'),
    # Deprecated: Dynamic service provider pages
    url(r'site/(?P<sds_id>[0-9]+)/$', views.detail_sds, name='detail_sds'), 

]