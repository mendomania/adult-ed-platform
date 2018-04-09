# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.forms import TextInput, Textarea
from .models import Outcome, Eligibility, Stream, Program, ServiceProvider, ProgramOutcome, ProgramEligibility, Offering

class OutcomeAdmin(admin.ModelAdmin):
    fields = ['text', 'colour']

class EligibilityAdmin(admin.ModelAdmin):
    fields = ['text']    

class StreamAdmin(admin.ModelAdmin):
    fields = ['text']

class ProgramAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Names',           {'fields': ['name_official', 'name_branding', 'code', 'colour']}),
        ('Introduction',    {'fields': ['header', 'intro1', 'intro2', 'video']}),
        ('Specifics',       {'fields': ['img_src1', 'img_txt1', 'img_src2', 'img_txt2', 'img_src3', 'img_txt3', 'img_src4', 'img_txt4']}),
        ('Key information', {'fields': ['is_available_online', 'offers_ossd_credits']}),
    ]   

class ServiceProviderAdmin(admin.ModelAdmin):
    fields = [
    'name', 'img_src', 'phone', 'email', 
    'address_street', 'address_city', 
    'address_province', 'address_zipcode', 
    'gps_lat', 'gps_lon'
    ] 

class OfferingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Foreign keys',    {'fields': ['program', 'service_provider', 'stream']}),
        ('Date & time',     {'fields': ['dow', 'str_date', 'end_date', 'str_time', 'end_time']}),
        ('Size',            {'fields': ['class_size']}),
        ('Perks',           {'fields': ['has_access_libraries', 'has_access_computers', 'has_childcare', 'has_counselling', 'has_employment', 'has_access_kitchen', 'has_access_parking', 'has_access_wheelchair']}),
    ]        

admin.site.register(Outcome, OutcomeAdmin)
admin.site.register(Eligibility, EligibilityAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(Stream, StreamAdmin)
admin.site.register(Offering, OfferingAdmin)

admin.site.register(ProgramOutcome)
admin.site.register(ProgramEligibility)

