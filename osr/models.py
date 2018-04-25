# -*- coding: utf-8 -*-
import os
from django.db import models
from django import forms
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey
from smart_selects.db_fields import ChainedManyToManyField

class Program(models.Model):
  name_official = models.CharField(max_length=50)
  name_branding = models.CharField(max_length=50)
  code = models.CharField(max_length=3, default="PRO")

  def __str__(self):
    return "%s - %s" % (self.name_official, self.code)    

  # Introduction
  header = models.CharField(max_length=200, blank=True)
  intro1 = models.TextField(max_length=200, blank=True, default="")
  intro2 = models.TextField(max_length=200, blank=True, default="")
  video = models.CharField(max_length=50, blank=True, default="")

  # Specifics about program
  img_src1 = models.ImageField(blank=True, null=True)
  img_txt1 = models.CharField(max_length=100, blank=True, default="")
  img_src2 = models.ImageField(blank=True, null=True)
  img_txt2 = models.CharField(max_length=100, blank=True, default="")
  img_src3 = models.ImageField(blank=True, null=True)
  img_txt3 = models.CharField(max_length=100, blank=True, default="")
  img_src4 = models.ImageField(blank=True, null=True)
  img_txt4 = models.CharField(max_length=100, blank=True, default="")      

  # Key elements
  is_available_online = models.BooleanField(default=False)
  offers_ossd_credits = models.BooleanField(default=False)

  # Colour
  colour = models.CharField(max_length=50, default="#000000")

class ServiceProvider(models.Model):
  name = models.CharField(max_length=50)
  # TODO: A user can only be linked to 1 SP
  # But a SP can have more than 1 user
  user = models.OneToOneField(User)
  programs = models.ManyToManyField('Program')

    # outcome = ChainedManyToManyField(
    # Outcome,
    # horizontal=True,
    # verbose_name='outcome',
    # chained_field="program",
    # chained_model_field="programs")
    
  def __str__(self):
    return self.name

  logo = models.ImageField(blank=True, null=True)
  phone = models.CharField(max_length=50, blank=True)
  email = models.CharField(max_length=50, blank=True)
  address_street = models.CharField(max_length=50, blank=True)
  address_city = models.CharField(max_length=30, blank=True)
  address_province = models.CharField(max_length=30, blank=True)
  address_zipcode = models.CharField(max_length=30, blank=True) 

class ServiceDeliverySite(models.Model):
  head = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.head.name + ": " + self.name

  phone = models.CharField(max_length=50, blank=True)
  email = models.CharField(max_length=50, blank=True)
  address_street = models.CharField(max_length=50, blank=True)
  address_city = models.CharField(max_length=30, blank=True)
  address_province = models.CharField(max_length=30, blank=True)
  address_zipcode = models.CharField(max_length=30, blank=True)
  gps_lat = models.FloatField(null=True, blank=True)
  gps_lon = models.FloatField(null=True, blank=True) 

class Outcome(models.Model):  
  text = models.CharField(max_length=200)
  colour = models.CharField(max_length=50, default="#000000")
  programs = models.ManyToManyField('Program')
  def __str__(self):
    return self.text  

class Eligibility(models.Model):
  text = models.CharField(max_length=200) 
  programs = models.ManyToManyField('Program') 
  def __str__(self):
    return self.text
  class Meta:
    verbose_name_plural = "eligibilities"

class Subject(models.Model):
  text = models.CharField(max_length=200)
  code = models.CharField(max_length=12, blank=True)
  programs = models.ManyToManyField('Program')
  def __str__(self):
    return self.text  

class Stream(models.Model):
  text = models.CharField(max_length=200)
  programs = models.ManyToManyField('Program')
  def __str__(self):
    return self.text  

CSIZE_RANGES = (('01', '1 - 10'),('02', '11 - 20'),('03', '20+'))
LEARN_STYLES = (('ON', 'Online'),('IN', 'In-person'),('BL', 'Blended'))
DAYS_OF_WEEK = (('Monday', 'Monday'),('Tuesday', 'Tuesday'),('Wednesday', 'Wednesday'),('Thursday', 'Thursday'),('Friday', 'Friday'),('Saturday', 'Saturday'),('Sunday', 'Sunday'))    

class Offering(models.Model):
  # Foreign keys
  program = models.ForeignKey(Program, on_delete=models.CASCADE)
  service_delivery_site = models.ForeignKey(ServiceDeliverySite, on_delete=models.CASCADE)
  str_date = models.DateField("Start date")
  end_date = models.DateField("End date")

  # TODO:
  class_size = models.CharField(max_length=2, choices=CSIZE_RANGES)
  learning_style = models.CharField(max_length=2, choices=LEARN_STYLES)

  outcomes = ChainedManyToManyField(
    Outcome,
    horizontal=True,
    verbose_name='outcomes',
    chained_field="program",
    chained_model_field="programs")

  requirements = ChainedManyToManyField(
    Eligibility,
    horizontal=True,
    verbose_name='requirements',
    chained_field="program",
    chained_model_field="programs")
    #chained_model_field="programs",
    #blank=True)

  streams = ChainedManyToManyField(
    Stream,
    horizontal=True,
    verbose_name='streams',
    chained_field="program",
    chained_model_field="programs")

  subjects = ChainedManyToManyField(
    Subject,
    horizontal=True,
    verbose_name='subjects',
    chained_field="program",
    chained_model_field="programs")          

  def __str__(self):
    return self.service_delivery_site.name + ": " + self.program

  def get_number_of_perks(self):
    for f in self.offeringfeature_set.all():
      print f
      print type(f)
    print self.offeringfeature_set.all().count()
    return "x" * (8 - self.offeringfeature_set.all().count())

  def get_number_of_outcomes(self):
    for f in self.outcomes.all():
      print f
      print type(f)
    return "x" * (8 - self.outcomes.all().count())

  def get_schedules(self):
    schedules = []
    print '[1] ********************* SCHEDULES *********************'
    print self.offeringschedule_set.all()
    for schedule in self.offeringschedule_set.all():
      print schedule
      schedules.append(str(schedule))
    print '[2] ********************* SCHEDULES *********************'
    print ', '.join(schedules)
    return ', '.join(schedules)

  clb_01 = models.BooleanField("CLB level 1", default=False)
  clb_02 = models.BooleanField("CLB level 2", default=False)
  clb_03 = models.BooleanField("CLB level 3", default=False)
  clb_04 = models.BooleanField("CLB level 4", default=False)
  clb_05 = models.BooleanField("CLB level 5", default=False)
  clb_06 = models.BooleanField("CLB level 6", default=False)
  clb_07 = models.BooleanField("CLB level 7", default=False)
  clb_08 = models.BooleanField("CLB level 8", default=False)
  clb_09 = models.BooleanField("CLB level 9", default=False)
  clb_10 = models.BooleanField("CLB level 10", default=False)
  clb_11 = models.BooleanField("CLB level 11", default=False)
  clb_12 = models.BooleanField("CLB level 12", default=False)  

  def __str__(self):
    return self.service_delivery_site.name + ": " + self.program.name_official + " - [" + str(self.str_date) + ", " + str(self.end_date) + "]"       

class OfferingSchedule(models.Model):
  offering = models.ForeignKey(Offering, on_delete=models.CASCADE)
  # days = models.CharField(max_length=1, choices=DAYS_OF_WEEK
  day_of_the_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
  str_time = models.TimeField("Start time")
  end_time = models.TimeField("End time")

  def __str__(self):    
    return self.day_of_the_week + ': ' + str(self.str_time)[:-3] + " to " + str(self.end_time)[:-3]

  # def get_outcomes(self):
  #   return ProgramOutcome.objects.filter(program__name_official=self.program.name_official)

  # def get_number_of_outcomes(self):
  #   num = 8 - len(ProgramOutcome.objects.filter(program__name_official=self.program.name_official))
  #   return "x" * num

class Profession(models.Model):
  text = models.CharField(max_length=60)
  def __str__(self):
    return self.text

class OfferingProfession(models.Model):
  offering = models.ForeignKey(Offering, on_delete=models.CASCADE)
  profession = models.ForeignKey(Profession, on_delete=models.CASCADE)
  def __str__(self):
    return self.offering.service_delivery_site.name + " - " + self.offering.program.code + ": " + self.profession.text

class Feature(models.Model):
  text = models.CharField(max_length=60)
  image = models.ImageField(blank=True, null=True)
  def __str__(self):
    return self.text

class OfferingFeature(models.Model):
  offering = models.ForeignKey(Offering, on_delete=models.CASCADE)
  feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
  def __str__(self):
    return self.offering.service_delivery_site.name + " - " + self.offering.program.code + ": " + self.feature.text

# class Continent(models.Model):
#   continent = models.CharField(max_length = 45)    
#   def __unicode__(self):
#     return unicode(self.continent)

# class Country(models.Model):
#   continent = models.ForeignKey(Continent)
#   country = models.CharField(max_length = 45)
#   def __unicode__(self):
#     return unicode(self.country)

# class Area(models.Model):
#   country = models.ForeignKey(Country)
#   area = models.CharField(max_length = 45)
#   def __unicode__(self):
#     return unicode(self.area)

# class Location(models.Model):
#   continent = models.ForeignKey(Continent)
#   country = ChainedForeignKey(Country, chained_field = "continent", chained_model_field = "continent", show_all = False, auto_choose = True)
#   area = ChainedForeignKey(Area, chained_field = "country", chained_model_field = "country")
#   city = models.CharField(max_length = 50)
#   street = models.CharField(max_length = 100)    

# class Publication(models.Model):
#     name = models.CharField(max_length=255)
#     def __str__(self):
#       return self.name

# class Writer(models.Model):
#     name = models.CharField(max_length=255)
#     publications = models.ManyToManyField('Publication', blank=True, null=True)
#     def __str__(self):
#       return self.name    

# class Book(models.Model):
#     publication = models.ForeignKey(Publication)
#     writer = ChainedManyToManyField(
#         Writer,
#         horizontal=True,
#         verbose_name='writer',
#         chained_field="publication",
#         chained_model_field="publications")
#     name = models.CharField(max_length=255)
#     def __str__(self):
#       return self.name        
