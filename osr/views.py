# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import loader
from .models import Offering, ProgramOutcome, Program, ProgramEligibility, Eligibility, Outcome
from django.views import generic
from django.db.models import Q
 

def search(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'osr/userlist.html', {'filter': user_filter})

def index(request):
    return HttpResponse("Hello, world. You're at the OSR index.")

class OfferingsView(generic.ListView):
  template_name = 'osr/offerings.html'
  context_object_name = 'all_offerings'
  paginate_by = 2

  def get_queryset(self):
    """ Return offerings """
    items = Offering.objects.order_by('str_date')  

    # Setting up filters...
    requirements = ProgramEligibility.objects.all();
    outcomes = ProgramOutcome.objects.distinct();
    programs = Program.objects.order_by('name_official').distinct('name_official')
    print '[R1]:', requirements

    print '%%%%%'
    print self.request.GET
    print items
    print '%%%%%'

    pro_filter = self.request.GET.getlist('program')
    print 'PRO:', pro_filter
    ele_filter = self.request.GET.getlist('e')
    print 'ELE:', ele_filter
    ser_filter = self.request.GET.getlist('s')
    print 'SER:', ser_filter
    fac_filter = self.request.GET.getlist('f')
    print 'FAC:', fac_filter
    out_filter = self.request.GET.getlist('o')
    print 'OUT:', out_filter

    # if not out_filter:
    #   print '*********************'
    #   print Offering.objects.none()

    # IF NO PROGRAMS SELECTED...? SHOW NOTHING?
    if pro_filter and pro_filter[0]:      
      print "YES - PRO"
      query = Q()
      # Filter offerings by programs selectec
      for val in pro_filter:
        query = query | Q(program=val)
      items = items.filter(query)
      print items

    if ele_filter and ele_filter[0]:      
      print "YES - ELE"
      query = Q()
      # Map eligibility requirements to programs
      for val in ele_filter:
        query = query | Q(eligibility_id=val)
      requirements = requirements.filter(query)      
      print '[R2]:', requirements

      if requirements:
        query = Q()
        # Filter offerings by programs selected
        for val in requirements:
          query = query | Q(program=val.program_id)
        items = items.filter(query)  
      else:
        print '*********************'
        print Offering.objects.none()
        return Offering.objects.none()

    # Filter support services
    if ser_filter and ser_filter[0]:
      print "YES - SER"
      for val in ser_filter:
        if val == '1':
          items = items.filter(has_childcare=True)
        if val == '2':
          items = items.filter(has_counselling=True)          
        if val == '3':
          items = items.filter(has_employment=True)  
      print items

    # Filter facilities
    if fac_filter and fac_filter[0]:
      print "YES - FAC"
      for val in fac_filter:
        if val == '1':
          items = items.filter(has_access_computers=True)
        if val == '2':
          items = items.filter(has_access_libraries=True)          
        if val == '3':
          items = items.filter(has_access_kitchen=True)                            
        if val == '4':
          items = items.filter(has_access_parking=True)                            
        if val == '5':
          items = items.filter(has_access_wheelchair=True)
      print items   

    # Filter outcomes
    if out_filter and out_filter[0]:  
      print "YES - OUT"    
      # Map outcomes to programs
      query = Q()
      for val in out_filter:
        query = query | Q(outcome_id=val)
      outcomes = outcomes.filter(query)  

      if outcomes:
        query = Q()
        # Filter
        for val in outcomes:
          query = query | Q(id=val.program_id)
        programs = programs.filter(query)  
      else:
        programs = Program.objects.none()

      if programs:
        query = Q()
        # Filter
        for val in programs:
          query = query | Q(program=val.id)
        items = items.filter(query) 
      else:
        print '*********************'
        print Offering.objects.none()
        return Offering.objects.none()
    else:
      print '*********************'
      print Offering.objects.none()
      return Offering.objects.none()

    print '*********************'
    print items
    return items


  def get_context_data(self, **kwargs):
    context = super(OfferingsView, self).get_context_data(**kwargs)
    context['count'] = self.get_queryset().count()
    context['all_outcomes'] = Outcome.objects.order_by('text').distinct('text')
    context['start'] = True

    # TODO
    outcomes = ProgramOutcome.objects.distinct();
    programs = Program.objects.order_by('name_official').distinct('name_official')
    out_filter = self.request.GET.getlist('o')

    print '----- GET:', out_filter
    if out_filter and out_filter[0]:    
      context['start'] = False  
      # Map outcomes to programs
      query = Q()
      for val in out_filter:
        query = query | Q(outcome_id=val)
      outcomes = outcomes.filter(query) 
      print '----- OUT:', outcomes 

      if outcomes:
        query = Q()
        # Filter
        for val in outcomes:
          query = query | Q(id=val.program_id)
        programs = programs.filter(query)  
        print '----- PRO:', programs
        context['all_programs'] = programs
      else:
        Program.objects.none()

    else:
      context['all_programs'] = Program.objects.order_by('name_official').distinct('name_official')


    context['all_eligibilities'] = Eligibility.objects.order_by('text').distinct('text')
    return context  

