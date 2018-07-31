# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db.models import Q
from .models import Program, ServiceProvider, ServiceDeliverySite, Outcome, Eligibility, Subject, Stream, Recommendation
from .models import Offering, OfferingSchedule, Profession, OfferingProfession, Feature, OfferingFeature
from .models import Facility, ServiceDeliverySiteFacility, ProgramRegistrationSteps, ProgramBestForScenarios
from .models import LearningOption, ScheduleOption, ProgramLinks, ImmigrationStatus, Benefit, ProfileSection
from .models import DictionaryEntry
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from django.utils.translation import ugettext_lazy as _

admin.site.site_header = _('My administration')

# Subsets
class AdminOfferingSchedule(admin.TabularInline):
  model = OfferingSchedule
  extra = 1  
  verbose_name_plural = _("Schedules")
  insert_after = "learning_style"

class AdminOfferingProfession(admin.TabularInline):
  model = OfferingProfession
  extra = 1   
  verbose_name_plural = _("Is this offering relevant to any specific professions?")
  insert_after = "learning_style"   

class AdminOfferingFeature(admin.TabularInline):
  model = OfferingFeature
  extra = 1        
  verbose_name_plural = _("Services provided")    
  insert_after = "learning_style"

class AdminServiceDeliverySiteFacility(admin.TabularInline):
  model = ServiceDeliverySiteFacility
  extra = 1        
  verbose_name_plural = _("Facilities")

class AdminProgramRegistrationSteps(TranslationTabularInline):
  model = ProgramRegistrationSteps
  extra = 1        
  verbose_name_plural = _("Registration steps")

class AdminProgramBestForScenarios(TranslationTabularInline):
  model = ProgramBestForScenarios
  extra = 1        
  verbose_name_plural = _("Best for scenarios") 

class AdminProgramProgramLinks(TranslationTabularInline):
  model = ProgramLinks
  extra = 1        
  verbose_name_plural = _("Useful external links")      

class AdminProgram(TranslationAdmin):
  fieldsets = [
    (_('BASIC INFORMATION'), {'fields': ['name_official', 'name_branding', 'code', 'order_id']}),
    (_('COLOURS'),       {'fields': ['marker', 'foreground_colour', 'background_colour']}),
    (_('TEXT FIELDS'),  {'fields': ['description', 'description_for_comparison_page', 'details', 'length', 'subsidies', 'support', 'funding', 'fees', 'free', 'types_of_sps']}),
    (_('KEY BENEFITS'),  {'fields': ['benefits']}),
    (_('OPTIONS'),  {'fields': ['learning_options', 'schedule_options']}),
    (_('ELIGIBLE IMMIGRATION STATUS'),  {'fields': ['eligible_immigration_status']}),
    (_('LOGO'),     {'fields': ['img_src', 'img_txt']})
  ]    
  inlines = [
    AdminProgramRegistrationSteps,
    AdminProgramBestForScenarios,
    AdminProgramProgramLinks
  ]

class AdminSP(admin.ModelAdmin):
  fieldsets = [
    (_('BASIC INFORMATION'), {'fields': ['name', 'logo']}),
    (_('REPRESENTATIVE OF SERVICE PROVIDER IN OUR SYSTEM'), {'fields': ['user']}),
    (_('CONTACT'), {'fields': ['phone', 'email']}),
    (_('ADDRESS'), {'fields': ['address_street', 'address_city', 'address_province', 'address_zipcode']}),
    (_('PROGRAMS'), {'fields': ['programs']}),
  ]
  # inlines = [AdminServiceProviderProgram]  

class AdminServiceDeliverySite(admin.ModelAdmin):
  fieldsets = [
    (_('MAIN BRANCH'), {'fields': ['head']}),
    (_('NAME OF SITE'), {'fields': ['name']}),
    (_('ADDRESS'), {'fields': ['address_street', 'address_city', 'address_province', 'address_zipcode']}),
  ]

  inlines = [
    AdminServiceDeliverySiteFacility
  ]

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
  fieldsets = [
    (_('BASIC INFORMATION'), {'fields': ['program', 'service_delivery_site', 'str_date', 'end_date', 'class_size', 'learning_style']}),
    (_('SPECIFIC SUBJECTS OF THIS OFFERING'), {'fields': ['subjects']}),
    (_('SPECIFIC OUTCOMES OF THIS OFFERING'), {'fields': ['outcomes']}),
    (_('SPECIFIC REQUIREMENTS OF THIS OFFERING'), {'fields': ['requirements']}),
    (_('SPECIFIC STREAMS OF THIS OFFERING'), {'fields': ['streams']}),
    (_('CLB LEVELS'), {'fields': ['clb_01', 'clb_02', 'clb_03', 'clb_04', 'clb_05', 'clb_06', 'clb_07', 'clb_08', 'clb_09', 'clb_10', 'clb_11', 'clb_12']}),
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

  def get_queryset(self, request):
    qs = super(AdminOffering, self).get_queryset(request)
    if request.user.is_superuser:
      return qs
    else: 
      # Find the service provider the logged in user belongs to
      providers = ServiceProvider.objects.filter(user=request.user.id)
      # Find the service delivery sites that service provider owns
      sites = ServiceDeliverySite.objects.filter(head__in=providers)      

      query = Q()
      # Show only offerings by those service delivery sites
      for site in sites:
        query = query | Q(service_delivery_site=site.id)
      return qs.filter(query)

  def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    field = super(AdminOffering, self).formfield_for_foreignkey(db_field, request, **kwargs)    

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

class OutcomeAdmin(TranslationAdmin):
  pass
class EligibilityAdmin(TranslationAdmin):
  pass
class StreamAdmin(TranslationAdmin):
  pass
class SubjectAdmin(TranslationAdmin):
  pass 
class ProfessionAdmin(TranslationAdmin):
  pass 
class FeatureAdmin(TranslationAdmin):
  pass  
class FacilityAdmin(TranslationAdmin):
  pass  
class RecommendationAdmin(TranslationAdmin):
  pass
class DictionaryEntryAdmin(TranslationAdmin):
  pass   
class ProfileSectionAdmin(TranslationAdmin):
  pass   
class LearningOptionAdmin(TranslationAdmin):
  pass  
class ScheduleOptionAdmin(TranslationAdmin):
  pass  
class ProgramLinksAdmin(TranslationAdmin):
  pass  
class ImmigrationStatusAdmin(TranslationAdmin):
  pass            
class BenefitAdmin(TranslationAdmin):
  pass              

admin.site.register(Program, AdminProgram)
admin.site.register(ServiceProvider, AdminSP)
admin.site.register(ServiceDeliverySite, AdminServiceDeliverySite)
admin.site.register(Offering, AdminOffering)

admin.site.register(Outcome, OutcomeAdmin)
admin.site.register(Eligibility, EligibilityAdmin)
admin.site.register(Stream, StreamAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(ProfileSection, ProfileSectionAdmin)
admin.site.register(LearningOption, LearningOptionAdmin)
admin.site.register(ScheduleOption, ScheduleOptionAdmin)
admin.site.register(ImmigrationStatus, ImmigrationStatusAdmin)
admin.site.register(Benefit, BenefitAdmin)
admin.site.register(DictionaryEntry, DictionaryEntryAdmin)