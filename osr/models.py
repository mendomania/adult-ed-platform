# -*- coding: utf-8 -*-
#import fields
from django.db import models

class Program(models.Model):
  name_official = models.CharField(max_length=50)
  name_branding = models.CharField(max_length=50)
  code = models.CharField(max_length=3, default="pro")

  def __str__(self):
    return self.name_official

  # Introduction
  header = models.CharField(max_length=200)
  intro1 = models.TextField(max_length=200)
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

class Outcome(models.Model):
  text = models.CharField(max_length=200)
  colour = models.CharField(max_length=50, default="#000000")
  def __str__(self):
    return self.text

class Eligibility(models.Model):
  text = models.CharField(max_length=200)  
  colour = models.CharField(max_length=50, default="#000000")  
  def __str__(self):
    return self.text
  class Meta:
        verbose_name_plural = "eligibilities"

class Stream(models.Model):
  text = models.CharField(max_length=200)
  def __str__(self):
    return self.text  

class ProgramOutcome(models.Model):
  program = models.ForeignKey(Program, on_delete=models.CASCADE)
  outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE)
  def __str__(self):
    return self.program.name_official + ": " + self.outcome.text

class ProgramEligibility(models.Model):
  program = models.ForeignKey(Program, on_delete=models.CASCADE)
  eligibility = models.ForeignKey(Eligibility, on_delete=models.CASCADE)  
  class Meta:
    verbose_name_plural = "program eligibilities"
  def __str__(self):
    return self.program.name_official + ": " + self.eligibility.text    

class ServiceProvider(models.Model):
  name = models.CharField(max_length=50)
    
  def __str__(self):
    return self.name

  img_src = models.ImageField(blank=True, null=True)
  phone = models.CharField(max_length=50)
  email = models.CharField(max_length=50)
  address_street = models.CharField(max_length=50)
  address_city = models.CharField(max_length=30)
  address_province = models.CharField(max_length=30)
  address_zipcode = models.CharField(max_length=30)
  gps_lat = models.FloatField(null=True, blank=True)
  gps_lon = models.FloatField(null=True, blank=True)

class Offering(models.Model):
  # Foreign keys
  program = models.ForeignKey(Program, on_delete=models.CASCADE)
  service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
  stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

  # Day of the week
  dow = models.CharField(max_length=50, default="Tuesday")

  # Dates and times
  str_date = models.DateField()
  end_date = models.DateField()
  str_time = models.TimeField()
  end_time = models.TimeField()

  def __str__(self):
    return self.service_provider.name + ": " + self.program.name_official + " - [" + str(self.str_date) + ", " + str(self.end_date) + "]"

  # Other
  class_size = models.SmallIntegerField()

  # Checkboxes
  has_access_libraries = models.BooleanField(default=False)
  has_access_computers = models.BooleanField(default=False)
  has_childcare = models.BooleanField(default=False)
  has_counselling = models.BooleanField(default=False)
  has_employment = models.BooleanField(default=False)
  has_access_kitchen = models.BooleanField(default=False)
  has_access_parking = models.BooleanField(default=False)
  has_access_wheelchair = models.BooleanField(default=False)

  def get_number_of_perks(self):
    num = 8 - (int(self.has_access_libraries) + int(self.has_access_computers) + int(self.has_childcare) + int(self.has_counselling) + int(self.has_employment) + int(self.has_access_kitchen) + int(self.has_access_parking) + int(self.has_access_wheelchair))
    return "x" * num

  def get_outcomes(self):
    return ProgramOutcome.objects.filter(program__name_official=self.program.name_official)

  def get_number_of_outcomes(self):
    num = 8 - len(ProgramOutcome.objects.filter(program__name_official=self.program.name_official))
    return "x" * num

  # Checkboxes...
  #days = fields.DayOfTheWeekField()
  #clbs = fields.CLBField()

  # Type...
