# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import loader
from .models import Offering, Program, Outcome, Eligibility, Feature
from django.views import generic
from django.db.models import Q
from django.db.models import Count
 
def index(request):
    return HttpResponse("Hello, world. You're at the OSR index.")

class WidgetView(generic.ListView):
  """ Widget cards """
  template_name = 'osr/widget.html'
  context_object_name = 'cards'

  def get_queryset(self):
    items = Program.objects.all();

class ResultsView(generic.ListView):
  """ Results of widget """
  template_name = 'osr/results.html'
  context_object_name = 'matches'

  def get_queryset(self):
    items = Program.objects.all();
    return items

  def get_context_data(self, **kwargs):
    context = super(ResultsView, self).get_context_data(**kwargs)
    pro_filter = self.request.GET.getlist('program')
    context['eslbool'] = False
    context['fslbool'] = False
    context['lbsbool'] = False
    context['adcbool'] = False
    context['acebool'] = False
    context['gedbool'] = False
    context['btpbool'] = False

    print 'PRO:', pro_filter

    if pro_filter and pro_filter[0]:
      for val in pro_filter:
        var = val.lower()        
        if var == 'esl':
          print '>>> ESL'
          context['eslbool'] = True
        if var == 'fsl':
          print '>>> FSL'
          context['fslbool'] = True
        if var == 'lbs':
          print '>>> LBS'
          context['lbsbool'] = True
        if var == 'adc':
          print '>>> ADC'
          context['adcbool'] = True
        if var == 'ace':
          print '>>> ACE'
          context['acebool'] = True
        if var == 'ged':
          print '>>> GED'
          context['gedbool'] = True                                                  
        if var == 'btp':
          print '>>> BTP'
          context['btpbool'] = True  
    return context                                                            

class OfferingsView(generic.ListView):
  template_name = 'osr/offerings.html'
  context_object_name = 'offerings'
  paginate_by = 5

  def get_queryset(self):
    """ Return offerings """
    items = Offering.objects.order_by('str_date') 

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
    out_filter = self.request.GET.getlist('o')
    print 'OUT:', out_filter

    programs = Program.objects.order_by('name_official')

    # Filter offerings by programs selected
    if pro_filter and pro_filter[0]:
      print ">>> YES - PRO"
      query = Q()
      for val in pro_filter:
        query = query | Q(program=val)
      items = items.filter(query)
    
    print ">>> END - PRO"
    print items

    print '-------------------------------------'
    for item in items:
      print item
      print '%%%%%%%%%%%%%%%%%'
      print type(item.requirements.all())
      for val in item.requirements.all():
        print val
        print val.id

    # Filter offerings by eligibility requirements selected
    if ele_filter and ele_filter[0]: 
      print ">>> YES - ELE"
      reqs = []
      for val in ele_filter:
        reqs.append(str(val))
      print reqs
      # In [30]: Photo.objects.filter(tags__in=[t1, t2]).annotate(num_tags=Count('tags')).filter(num_tags=2)
      items = items.filter(requirements__in=reqs)
      # AND: items = items.filter(requirements__in=reqs).annotate(num_reqs=Count('requirements')).filter(num_reqs=len(reqs))
    print ">>> END - ELE"
    print items

    # Filter offerings by support services
    if ser_filter and ser_filter[0]:
      print ">>> YES - SER"
      sers = []
      for val in ser_filter:
        sers.append(str(val))
      print sers
      #items.offeringfeature_set.filter(feature_id__in=sers);
      #items.filter(offeringfeature_set_in=reqs)
      #for val in ser_filter:

      items = items.filter(offeringfeature__feature_id__in=sers)
    print ">>> END - SER"       
    print items
 
    # Filter offerings by outcomes selected
    if out_filter and out_filter[0]: 
      print ">>> YES - OUT"
      outs = []
      for val in out_filter:
        outs.append(str(val))
      print outs
      # In [30]: Photo.objects.filter(tags__in=[t1, t2]).annotate(num_tags=Count('tags')).filter(num_tags=2)
      # AND: items = items.filter(outcomes__in=outs).annotate(num_outs=Count('outcomes')).filter(num_outs=len(outs))
      items = items.filter(outcomes__in=outs)
    else:
      items = Offering.objects.none()

    print ">>> END - OUT"

    print '*********************'
    items = items.distinct();
    print items
    services = []
    for item in items:
      for service in item.offeringfeature_set.all():
        services.append(service.id)
    print '*********************'

    return items

  def get_context_data(self, **kwargs):
    context = super(OfferingsView, self).get_context_data(**kwargs)

    # Init
    context['start'] = True
    context['count'] = self.get_queryset().count()
    context['outcomes'] = Outcome.objects.order_by('text')
    context['programs'] = Program.objects.none()
    context['eligibilities'] = Eligibility.objects.none();
    context['eligibilities'] = Feature.objects.none();

    out_filter = self.request.GET.getlist('o')

    # >>> From OUTCOMEs let's get PROGRAMs and ELIGIBILITIEs
    outcomes = Outcome.objects.all();
    print '@@@@@@@@@@@@@@@@@@@@@'
    print outcomes
    print '@@@@@@@@@@@@@@@@@@@@@'
    print '@@@@@@@@@@@@@@@@@@@@@'

    print '----- GET:', out_filter
    if out_filter and out_filter[0]:
      context['start'] = False   
      # Filter outcomes    
      query = Q()
      for val in out_filter:
        query = query | Q(id=val)
      outcomes = outcomes.filter(query) 
      print '----- OUT:', outcomes 

      if outcomes:
        programs = Program.objects.none();
        requirements = Eligibility.objects.none();
        features = Feature.objects.all();
        for outcome in outcomes:
          programs = (programs | outcome.programs.all())
        print '----- PRO:', programs
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        query = Q()
        for program in programs:
          requirements = (requirements | program.eligibility_set.all())
          for offering in program.offering_set.all():
            for val in offering.offeringfeature_set.all():
              query = query | Q(id=val.feature.id)
        features = features.filter(query)
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print '----- FEA:', features
        print '----- REQ:', requirements

        context['features'] = features.order_by('text').distinct()
        context['programs'] = programs.order_by('name_official').distinct()
        context['eligibilities'] = requirements.order_by('text').distinct()

    return context  
