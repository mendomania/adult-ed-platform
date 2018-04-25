# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.forms import TextInput, Textarea
#from .models import Outcome, Program, ServiceProvider, Outcome, Offering, ServiceDeliverySite, Profession, Feature, OfferingSchedule, OfferingProfession, OfferingFeature, ServiceProviderProgram#, Eligibility, Stream, Subject, ProgramEligibility, ProgramStream, ProgramSubject, OfferingStream, OfferingEligibility, OfferingSubject, OfferingOutcome
from django.db.models import Q
from .forms import OfferingForm
#from .models import Continent, Country, Area, Location, Publication, Writer, Book
from .models import Program, ServiceProvider, ServiceDeliverySite, Outcome, Eligibility, Subject, Stream
from .models import Offering, OfferingSchedule, Profession, OfferingProfession, Feature, OfferingFeature

admin.site.site_header = 'My administration'

# Subsets
class AdminOfferingProgram(admin.ModelAdmin):
  fields = ['program']

class AdminProfession(admin.ModelAdmin):
  fields = ['text']

class AdminFeature(admin.ModelAdmin):
  fields = ['text']   

# Program
class AdminProgram(admin.ModelAdmin):
  fieldsets = [
    ('Names',       {'fields': ['name_official', 'name_branding', 'code', 'colour']}),
    ('Introduction',  {'fields': ['header', 'intro1', 'intro2', 'video']}),
    ('Specifics',     {'fields': ['img_src1', 'img_txt1', 'img_src2', 'img_txt2', 'img_src3', 'img_txt3', 'img_src4', 'img_txt4']}),
    ('Key information', {'fields': ['is_available_online', 'offers_ossd_credits']}),
  ]    

class AdminOfferingSchedule(admin.TabularInline):
  model = OfferingSchedule
  extra = 1  
  verbose_name_plural = "Schedules"    
  insert_after = "learning_style"

class AdminOfferingProfession(admin.TabularInline):
  model = OfferingProfession
  extra = 1   
  verbose_name_plural = "Is this offering relevant to any specific professions?" 
  insert_after = "learning_style"   

class AdminOfferingFeature(admin.TabularInline):
  model = OfferingFeature
  extra = 1        
  verbose_name_plural = "Services provided"    
  insert_after = "learning_style"

class AdminSP(admin.ModelAdmin):
  fieldsets = [
    ('BASIC INFORMATION', {'fields': ['name', 'logo']}),
    ('REPRESENTATIVE OF SERVICE PROVIDER IN OUR SYSTEM', {'fields': ['user']}),
    ('CONTACT', {'fields': ['phone', 'email']}),
    ('ADDRESS', {'fields': ['address_street', 'address_city', 'address_province', 'address_zipcode']}),
    ('PROGRAMS', {'fields': ['programs']}),
  ]
  # inlines = [AdminServiceProviderProgram]  

class AdminServiceDeliverySite(admin.ModelAdmin):

  def get_queryset(self, request):
    qs = super(AdminServiceDeliverySite, self).get_queryset(request)
    if request.user.is_superuser:
      return qs
    else: 
      # Find the service provider the logged in user belongs to
      providers = ServiceProvider.objects.filter(user=request.user.id)
      query = Q()
      # Show only delivery sites owned by this service provider
      for provider in providers:
        query = query | Q(head=provider)
      return qs.filter(query)

  def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    field = super(AdminServiceDeliverySite, self).formfield_for_foreignkey(db_field, request, **kwargs)    
    if db_field.name == 'head':
      u = request.user
      # The service provider field in the admin page will be filtered out
      if not u.is_superuser:
        field.queryset = field.queryset.filter(user=u.id)
    return field

class AdminOffering(admin.ModelAdmin):
  #form = OfferingForm
  fieldsets = [
    ('BASIC INFORMATION', {'fields': ['program', 'service_delivery_site', 'str_date', 'end_date', 'class_size', 'learning_style']}),
    ('SPECIFIC SUBJECTS OF THIS OFFERING', {'fields': ['subjects']}),
    ('SPECIFIC OUTCOMES OF THIS OFFERING', {'fields': ['outcomes']}),
    ('SPECIFIC REQUIREMENTS OF THIS OFFERING', {'fields': ['requirements']}),
    ('SPECIFIC STREAMS OF THIS OFFERING', {'fields': ['streams']}),
    ('CLB LEVELS', {'fields': ['clb_01', 'clb_02', 'clb_03', 'clb_04', 'clb_05', 'clb_06', 'clb_07', 'clb_08', 'clb_09', 'clb_10', 'clb_11', 'clb_12']}),
  ]
  inlines = [
    AdminOfferingProfession, 
    AdminOfferingSchedule, 
    AdminOfferingFeature
  ]  
  class Media:
    js = { 'admin/js/offering_admin.js' }
    # css = {
    #   'all': (
    #     'admin/css/admin.css',
    #   )
    # }  
  
  def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    field = super(AdminOffering, self).formfield_for_foreignkey(db_field, request, **kwargs)    

    print '+++++++++++++++++++++ [FOREIGN-KEY] +++++++++++++++++++++'

    # Filter programs
    if db_field.name == 'program':
      u = request.user      
      if not u.is_superuser:
        # Find the service provider the logged in user belongs to
        providers = ServiceProvider.objects.filter(user=request.user.id)
        programs = Program.objects.none();
        for provider in providers:
          # Union
          programs = (programs | provider.programs.all())
        # Find the programs such service provider is authorized to offer
        field.queryset = programs

    # Filter service delivery sites
    if db_field.name == 'service_delivery_site':
      u = request.user      
      if not u.is_superuser:
        # Find the service provider the logged in user belongs to
        providers = ServiceProvider.objects.filter(user=u.id)
        query = Q()
        # Show only delivery sites owned by this service provider
        for provider in providers:
          query = query | Q(head=provider)
        field.queryset = field.queryset.filter(query)

    return field

admin.site.register(Program)
admin.site.register(ServiceProvider, AdminSP)
admin.site.register(ServiceDeliverySite, AdminServiceDeliverySite)

admin.site.register(Outcome)
admin.site.register(Eligibility)
admin.site.register(Stream)
admin.site.register(Subject)

admin.site.register(Offering, AdminOffering)
admin.site.register(Profession)
admin.site.register(Feature)

# admin.site.register(Continent)
# admin.site.register(Country)
# admin.site.register(Area)
# admin.site.register(Location)

# admin.site.register(Publication)
# admin.site.register(Writer)
# admin.site.register(Book)