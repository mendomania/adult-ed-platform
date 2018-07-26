# -*- coding: utf-8 -*-
import json
import codecs
import os.path
from datetime import datetime
from django.views import generic
from django.db.models import Q
from django.urls import reverse
from django.utils import translation
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from easy_pdf.views import PDFTemplateView
from .models import Offering, Program, Outcome, Eligibility, Feature, Facility, ServiceDeliverySite, Recommendation

###########################################################################################
#####                                      ALPHA                                      #####
###########################################################################################

def intro(request):
  """ 
  This view corresponds to the adult learning landing page.
  This page will show brief descriptions of all available programs.
  """

  # All available programs
  programs = Program.objects.all() 
  paramLang = "?lang=%s" % (translation.get_language())
  return render(request, 'osr/intro.html', {'programs': programs, 'paramLang': paramLang})

def detail_program(request, program_code):
  """ 
  This view corresponds to the dynamic program pages.
  There is a program page for each program in the DB.
  This page will show details about each program.
  """  
  program = get_object_or_404(Program, code=program_code.upper())

  # Set language
  set_lang(request)

  return render(request, 'osr/program.html', {'program': program})  

def matchmaker(request):
  """ 
  This view corresponds to the matchmaker page.
  This page will present the user with a series of questions.
  """

  # Set language
  set_lang(request)

  return render(request, 'osr/matchmaker.html') 

def transition(request):
  """ 
  This view corresponds to the results page that is shown to the user at the end of the matchmaker.
  This page will present the user with:
  1. The programs that best match their needs and goals
  2. A set of recommendations that are relevant to their situation
  3. A summary of other information that was captured from the user
  It will also store some variables in the cache, to be re-used by other views.  
  """ 

  # Matching programs will be stored in different lists to be easily displayed in the page
  groupOf1s, groupOf2s, groupOf3s = [], [], []
  programs = Program.objects.all()

  # Recommendations will be retrieved from the DB
  recommendations = Recommendation.objects.none()

  # Variables used to display a message when the user chooses to e-mail themselves their results
  wasEmailSent = False
  emailAddress = ''

  # This variable will show or hide the section of the results page that shows matching programs
  showMatchingPrograms = False

  if request.method == "GET":
    print "***** [TRANSITION]-[G]"
    if 'wasEmailSent' in request.session and 'emailAddress' in request.session:
      wasEmailSent = True
      emailAddress = request.session['emailAddress']

    # If there are cached vars then proceed normally
    if 'matches' in request.session:
      showMatchingPrograms = True
      programs = get_program_matches_from_cache(request)
      recommendations = get_recommendations_from_cache(request)
      groupOf1s, groupOf2s, groupOf3s, paramsPrograms = group_programs(programs)
    # If there are no cached vars then redirect user to the matchmaker page  
    else:
      return redirect('/osr/matchmaker/')

  if request.method == "POST":
    print "***** [TRANSITION]-[P]"      
    # Create dictionary from JSON created during the matchmaker experience
    dico = json.loads(request.POST.get("dico", "").encode('utf-8'))
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    print dico
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

    reset_cache(request) 
    translation.activate(dico['lang'])    

    # Save program matches to cache
    programs = save_program_matches_to_cache(dico, request)
    # Group programs
    groupOf1s, groupOf2s, groupOf3s, paramsPrograms = group_programs(programs)
    # Save recommendations to cache
    recommendations = save_recommendations_to_cache(dico, request)
    # Save learner profile to cache
    save_learner_profile_to_cache(dico, request)

  paramLang = "?lang=%s" % (translation.get_language())

  return render(request, 'osr/transition.html', 
    {'number': programs.count, 'groupOf1s': groupOf1s, 'groupOf2s': groupOf2s, 'groupOf3s': groupOf3s, 
     'paramsPrograms': paramsPrograms, 'paramLang': paramLang, 'recommendations': recommendations, 
     'showMatchingPrograms': showMatchingPrograms, 'wasEmailSent': wasEmailSent, 'emailAddress': emailAddress})

def comparison(request):
  """ 
  This view corresponds to the comparison page.
  This page will present the user with a carousel showing programs to be compared.
  """

  # Show all programs by default
  programs = Program.objects.all()

  # If some programs are passed as parameters then show only those programs
  pro_filter = request.GET.getlist('p')
  if pro_filter and pro_filter[0]:
    query = Q()
    for val in pro_filter:
      query = query | Q(code=val)
    programs = programs.filter(query)  

  # Set language
  set_lang(request)
  paramLang = "?lang=%s" % (translation.get_language())

  return render(request, 'osr/comparison.html', {'programs': programs, 'paramLang': paramLang})

def set_lang(request):
  """ Set language that was passed in as a parameter in the URL """  
  lan_filter = request.GET.getlist('lang')
  if lan_filter and lan_filter[0]:
    translation.activate(lan_filter[0])  

class ResultsPDFView(PDFTemplateView):
  """ 
  This view is triggered when a user clicks the "Download PDF" button in the results page.
  It is used to create a PDF with the results of the matchmaker for a particular user.
  The info to be included in the PDF is retrieved from the cache. 
  """  
  pdf_filename = 'results.pdf'
  template_name = 'osr/print.html'  

  def get_context_data(self, **kwargs):
    context = super(ResultsPDFView, self).get_context_data(pagesize = "A4", title = "My results", **kwargs)

    # Retrieve information from cache
    matches = get_program_matches_from_cache(self.request)
    recommendations = get_recommendations_from_cache(self.request)
    
    # Variables to be passed in to the HTML to render the PDF
    context['matches'] = matches
    context['recommendations'] = recommendations
    context['program_path'] = "%s://%s%s" % (self.request.scheme, self.request.get_host(), "/osr/program")
    context['results_path'] = "%s://%s%s" % (self.request.scheme, self.request.get_host(), reverse('osr:transition'))
    return context

def email(request):
  """ 
  This view is triggered when a user clicks the "Get results by e-mail" button in the results page.
  It is used to create the HTML message of an e-mail with the results of the matchmaker for a user.
  The info to be included in the e-mail is retrieved from the cache.
  """  

  # If an email address was provided
  params = request.GET.getlist('emailAddress')
  if params and params[0]:
    email_address = params[0]

    # Retrieve information from cache
    matches = get_program_matches_from_cache(request)
    recommendations = get_recommendations_from_cache(request)

    # Variables to be included in the email
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    program_path = "%s://%s%s" % (request.scheme, request.get_host(), "/osr/program")
    results_path = "%s://%s%s" % (request.scheme, request.get_host(), reverse('osr:transition'))
    number_programs = '%d program' % (len(matches)) if (len(matches) == 1) else '%d programs' % (len(matches))

    # Load template of HTML message with placeholders
    curr_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(curr_path, "templates/osr/email.html")
    html_base = codecs.open(file_path, 'r', encoding='utf-8')

    # Fill in placeholders in HTML message
    code_program_matches = ''
    for m in matches:
      match = "<tr><td><b>%s</b></td><td>%s<br/>%s/%s</td></tr>" % (m.name_official, m.description, program_path, m.code.lower())
      code_program_matches = code_program_matches + match
    code_recommendations = ''
    for r in recommendations:
      recommendation = "<tr><td>%s</td><td>%s<br/>%s</td></tr>" % (r.reason, r.text, r.link)      
      code_recommendations = code_recommendations + recommendation
    html_message = html_base.read() % (number_programs, code_program_matches, code_recommendations, results_path, timestamp)
        
    send_mail(
      subject = 'Your results and recommendations',
      message = "",
      html_message = html_message,
      from_email = 'noreply@codefor.ca',
      recipient_list = [email_address],
      fail_silently = False,
    )

    request.session['wasEmailSent'] = True
    request.session['emailAddress'] = email_address

  return redirect('/osr/transition/')

def group_programs(programs):
  """ 
  This view corresponds to the comparison page.
  This page will present the user with a carousel showing programs to be compared.
  """

  # Matching programs will be stored in different lists to be easily displayed in the page
  groupOf1s, groupOf2s, groupOf3s = [], [], []
  prog_url = ''

  # Create program parameters
  proglist = []
  for program in programs:
    proglist.append(program)   
    prog_url = prog_url + '&p=' + program.code
  num = len(proglist)

  # Code used to format programs:
  # The layout of "transition.html" allows for up to 3 programs per row
  # groupOf1s = To be used when there is 1 matching program
  # groupOf2s = To be used when there are 2 or (3+ AND not a multiple of 3) matching programs  
  # groupOf3s = To group 3 programs per row  

  # Number of programs: [01]
  if num == 1:
    groupOf1s = proglist
  # Number of programs: [02]        
  elif num == 2:
    groupOf2s = [{ 'tup1': proglist[-2], 'tup2': proglist[-1] }]
  else:
    # Number of programs: [03, 06, 09...]
    if num % 3 == 0:
      groupOf3s = proglist
    # Number of programs: [04, 07, 10...]
    elif num % 3 == 1:                  
      # Last 4 matches
      groupOf2s = [{ 'tup1': proglist[-4], 'tup2': proglist[-3] }, { 'tup1': proglist[-2], 'tup2': proglist[-1] }]
      # All other matches (which will be a multiple of 3)
      groupOf3s = proglist[0:-4]
    # Number of programs: [05, 08, 11...]
    else:
      # Last 2 matches
      groupOf2s = [{ 'tup1': proglist[-2], 'tup2': proglist[-1] }]
      # All other matches (which will be a multiple of 3)
      groupOf3s = proglist[0:-2] 

  return (groupOf1s, groupOf2s, groupOf3s, prog_url)

###########################################################################################
#####                                      TODO                                       #####
###########################################################################################

def filter_recommendations(recolist):
  if not recolist:
    return Recommendation.objects.none()
  else:
    recommendations = Recommendation.objects.all()
    query = Q()
    for code in recolist:
      query = query | Q(code=code)
    recommendations = recommendations.filter(query)         
    print recommendations  
    return recommendations

def filter_program_matches(codelist):
  if not codelist:
    return Program.objects.none()
  else:
    programs = Program.objects.all()
    query = Q()
    for code in codelist:
      query = query | Q(code=code)
    programs = programs.filter(query)   
    print programs
    return programs

###########################################################################################
#####                                      TODO                                       #####
###########################################################################################

def save_program_matches_to_cache(dico, request):
  codelist = []
  if 'matches' not in request.session:
    request.session['matches'] = []

  # Language programs
  if 'program_lang' in dico and 'lang_target' in dico:
    if dico['lang_target'] == 'English':
      codelist.append('ESL')
      request.session['matches'].append('ESL')
    if dico['lang_target'] == 'French':
      codelist.append('FSL')
      request.session['matches'].append('FSL')

  # LBS
  if 'program_upgr' in dico:
    codelist.append('LBS')
    request.session['matches'].append('LBS')

  # Credential programs 
  if 'program_cert' in dico:
    codelist.append('ADC')
    request.session['matches'].append('ADC')     
  if 'hs_goal_work' in dico or 'hs_goal_university' in dico or 'hs_goal_college' in dico:
    codelist.append('GED')
    request.session['matches'].append('GED')  
    if 'ADC' not in codelist:
      codelist.append('ADC')
      request.session['matches'].append('ADC') 

  # BTP 
  if 'program_obtp' in dico:
    codelist.append('BTP')
    request.session['matches'].append('BTP') 

  print codelist
  return filter_program_matches(codelist)

###########################################################################################
#####                                      TODO                                       #####
###########################################################################################

def save_recommendations_to_cache(dico, request):
  recolist = []
  # TODO:
  # if 'lang_skill_writing' in dico:
  #   recolist.append('lang_skill_writing')
  #   request.session['lang_skill_writing'] = 'T'
  # if 'lang_skill_reading' in dico:
  #   recolist.append('lang_skill_reading')
  #   request.session['lang_skill_reading'] = 'T'
  # if 'lang_skill_listening' in dico:
  #   recolist.append('lang_skill_listening')
  #   request.session['lang_skill_listening'] = 'T'
  # if 'lang_skill_speaking' in dico:
  #   recolist.append('lang_skill_speaking')    
  #   request.session['lang_skill_speaking'] = 'T'

  if 'hs_goal_apprenticeship' in dico:
    recolist.append('apprenticeship')
    request.session['apprenticeship'] = 'T'

  if 'plar' in dico:
    recolist.append('plar')
    request.session['plar'] = 'T'

  if 'status_pr' in dico:
    recolist.append('status_pr')
    request.session['status_pr'] = 'T'

  if 'hs_goal_work' in dico:
    recolist.append('hs_goal_work')
    request.session['hs_goal_work'] = 'T'        

  print ">>> RECOMMENDATION CODEs"
  print recolist        
  return filter_recommendations(recolist)

def save_learner_profile_to_cache(dico, request):
  # PROFILE_BASIC  
  if 'age' in dico:
    request.session['profile_basic_age'] = "You are %s years old" % (dico['age'])
  if 'ontario_resident' in dico:
    if dico['ontario_resident'] == 'T':
      request.session['profile_basic_ontario_resident'] = 'You are a resident of Ontario'
    if dico['ontario_resident'] == 'F':
      request.session['profile_basic_ontario_resident'] = 'You are not a resident of Ontario'    

  if 'status_can_citizen' in dico:
    request.session['profile_basic_immigration_status'] = 'You were born in Canada'
  if 'status_nat_citizen' in dico:
    request.session['profile_basic_immigration_status'] = 'You are a naturalized citizen'
  if 'status_pr' in dico:
    request.session['profile_basic_immigration_status'] = 'You are a permanent resident'
  if 'status_refugee' in dico:
    request.session['profile_basic_immigration_status'] = 'You are a convention refugee'                
  if 'status_claimant' in dico:
    request.session['profile_basic_immigration_status'] = 'You are a refugee claimant'
  if 'status_approval' in dico:
    request.session['profile_basic_immigration_status'] = 'You have a letter of initial approval of PR from Citizenship and Immigration Canada'                        
  if 'status_caregiver' in dico:
    request.session['profile_basic_immigration_status'] = 'You are a foreign domestic worker admitted under the Live-In Caregiver Program'                            
  if 'status_nominee' in dico:
    request.session['profile_basic_immigration_status'] = 'You are a provincial nominee approved through Opportunities Ontario Provincial Nominee Program'                                

  if 'lang_source' in dico:
    lan = ''
    if dico['lang_source'] == 'Other':
      lan = 'not English nor French'
    else:
      lan = dico['lang_source']
    request.session['profile_basic_lang_source'] = "Your native language is %s" % (lan)

  if 'hs_complete' in dico: 
    if 'plar' in dico:
      request.session['highschool'] = "You completed high school outside of Ontario" 
    else:
      request.session['highschool'] = "You completed high school in Ontario" 
  elif 'hs_incomplete' in dico:  
    if 'plar' in dico:
      request.session['highschool'] = "You have incomplete high school studies from outside of Ontario" 
    else:
      request.session['highschool'] = "You have incomplete high school studies in Ontario" 
  else:
    request.session['highschool'] = "You have not previously attended high school" 

  if 'has_ossd' in dico:
    request.session['ossd'] = "You have an OSSD"    
  elif 'has_ossc' in dico:
    request.session['ossd'] = "You have an OSSC"
  else: 
    request.session['ossd'] = "You have neither an OSSD nor an OSSC"

  if 'has_ged' in dico:
    request.session['gedx'] = "You have a GED"
  else: 
    request.session['gedx'] = "You don't have a GED"

  if 'international_edu' in dico:
    request.session['intl_edu'] = "You have a post-secondary certificate or degree from outside of Canada"    
  if 'international_job' in dico:
    request.session['intl_job'] = "You have international work experience"        

  goals = []
  if 'goal_language' in dico and 'lang_target' in dico:
    subs = []
    if 'lang_reason_everyday' in dico:
      subs.append('for everyday communication')
    if 'lang_reason_studies' in dico:
      subs.append('to prepare for future studies') 
    if 'lang_reason_employment' in dico:
      subs.append('prepare for employment') 
    if 'lang_reason_citizenship' in dico:
      subs.append('prepare for the citizenship test') 
    if 'lang_reason_tests' in dico:
      subs.append('prepare for language tests') 
    if 'lang_reason_ossd' in dico:
      subs.append('prepare to get your OSSD')                              
    txt = "Improve your %s for %s" % (dico['lang_target'], ', '.join(subs))    
    goals.append(txt)
  if 'goal_highschool' in dico:    
    subs = []
    if 'hs_goal_work' in dico:
      subs.append('work')
    if 'hs_goal_university' in dico:
      subs.append('university')      
    if 'hs_goal_college' in dico:
      subs.append('college')            
    if 'hs_goal_apprenticeship' in dico:
      subs.append('apprenticeship')    
    txt = 'Get a highschool diploma or equivalent certificate for %s' % (', '.join(subs))              
    goals.append(txt)
  if 'goal_upgrade_credits_marks' in dico:
    subs = []
    if 'hs_goal_work' in dico:
      subs.append('work')
    if 'hs_goal_university' in dico:
      subs.append('university')      
    if 'hs_goal_college' in dico:
      subs.append('college')            
    if 'hs_goal_apprenticeship' in dico:
      subs.append('apprenticeship')    
    txt = 'Get missing credits or upgrade marks for %s' % (', '.join(subs)) 
    goals.append(txt)    
  if 'goal_refresh_skills' in dico:
    subs = []
    if 'refresh_reason_everyday' in dico:
      subs.append('for self-improvement')
    if 'refresh_reason_employment' in dico:
      subs.append('for better employment opportunities')      
    if 'refresh_reason_studies' in dico:
      subs.append('in preparation for further education')              
    txt = 'Develop or refresh your skills %s' % (', '.join(subs))
    goals.append(txt)
  if 'goal_canadian_xp' in dico:    
    goals.append('Adapt international professional or trade work experience to Canada')
  request.session['main_goals'] = goals

  lans = 'You want to get better at %s'
  subs = []
  if 'lang_skill_listening' in dico:
    if dico['lang_source'] == 'ASL' or dico['lang_target'] == 'ASL':
      subs.append('understanding ASL signs')
    else:
      subs.append('listening')
  if 'lang_skill_speaking' in dico:
    if dico['lang_source'] == 'ASL' or dico['lang_target'] == 'ASL':
      subs.append('signing ASL')
    else:
      subs.append('speaking') 
  if 'lang_skill_reading' in dico:
    subs.append('reading')          
  if 'lang_skill_writing' in dico:
    subs.append('writing')
  if 'skill_math' in dico:
    subs.append('doing math')          
  if 'skill_computer' in dico:
    subs.append('using the computer')    
  request.session['need_goals'] = lans % (', '.join(subs))

# Get me matches from dico
def get_program_matches_from_cache(request):
  # Program matches
  codelist = []
  if 'matches' in request.session:
    for match in request.session['matches']:
      codelist.append(match)
  print codelist
  return filter_program_matches(codelist)
  #print recolist    
  #return filter_recommendations(recolist)

# Get me recommendations from dico
def get_recommendations_from_cache(request):
  # Recommendations
  recolist = []
  # TODO:
  # if 'lang_skill_writing' in request.session:
  #   recolist.append('lang_skill_writing')
  # if 'lang_skill_reading' in request.session:
  #   recolist.append('lang_skill_reading')
  # if 'lang_skill_speaking' in request.session:
  #   recolist.append('lang_skill_speaking')
  # if 'lang_skill_listening' in request.session:
  #   recolist.append('lang_skill_listening')

  if 'apprenticeship' in request.session:
    recolist.append('apprenticeship')
  if 'plar' in request.session:
    recolist.append('plar')  
  if 'status_pr' in request.session:
    recolist.append('status_pr')        
  if 'hs_goal_work' in request.session:
    recolist.append('hs_goal_work')            
 
  print '########### RECO LIST #########'
  print recolist    
  return filter_recommendations(recolist)

def reset_cache(request):
  """ Delete all variables stored in the cache """
  for key in request.session.keys():
    print key, request.session[key]
    del request.session[key]  

###########################################################################################
#####                                      BETA                                       #####
###########################################################################################

def detail_sds(request, sds_id):
  service_delivery_site = get_object_or_404(ServiceDeliverySite, id=sds_id)
  return render(request, 'osr/sds.html', {'sds': service_delivery_site})     

class OfferingsView(generic.ListView):
  template_name = 'osr/offerings.html'
  context_object_name = 'offerings'
  paginate_by = 5

  def get_queryset(self):
    """ Return offerings """
    items = Offering.objects.order_by('-id')

    pro_filter = self.request.GET.getlist('program')
    print 'PRO:', pro_filter
    ele_filter = self.request.GET.getlist('e')
    print 'ELE:', ele_filter
    fea_filter = self.request.GET.getlist('f')
    print 'FEA:', fea_filter
    ser_filter = self.request.GET.getlist('s')
    print 'SER:', ser_filter
    out_filter = self.request.GET.getlist('o')
    print 'OUT:', out_filter

    programs = Program.objects.order_by('name_official')

    # Filter offerings by programs selected
    if pro_filter and pro_filter[0]:
      query = Q()
      for val in pro_filter:
        query = query | Q(program=val)
      items = items.filter(query)

    # Filter offerings by eligibility requirements selected
    if ele_filter and ele_filter[0]:
      reqs = []
      for val in ele_filter:
        reqs.append(str(val))
      print reqs
      for req in reqs:
        items = items.filter(requirements__id=req)   
    print items

    # Filter offerings by features
    if fea_filter and fea_filter[0]:
      feas = []
      for val in fea_filter:
        feas.append(str(val))
      print feas
      for fea in feas:
        items = items.filter(offeringfeature__feature_id=fea)
    print items

    # Filter offerings by services (facilities)
    if ser_filter and ser_filter[0]:
      sers = []
      for val in ser_filter:
        sers.append(str(val))
      print sers
      #items = items.filter(service_delivery_site__servicedeliverysitefacility__facility_id__in=sers)
      for ser in sers:
        items = items.filter(service_delivery_site__servicedeliverysitefacility__facility_id=ser)

    # Filter offerings by outcomes selected
    if out_filter and out_filter[0]:
      outs = []
      for val in out_filter:
        outs.append(str(val))
      print outs
      # In [30]: Photo.objects.filter(tags__in=[t1, t2]).annotate(num_tags=Count('tags')).filter(num_tags=2)
      # AND: items = items.filter(outcomes__in=outs).annotate(num_outs=Count('outcomes')).filter(num_outs=len(outs))
      items = items.filter(outcomes__in=outs)
    else:
      items = Offering.objects.none()

    items = items.distinct();
    print items
    services = []
    for item in items:
      for service in item.offeringfeature_set.all():
        services.append(service.id)

    return items

  def get_context_data(self, **kwargs):
    context = super(OfferingsView, self).get_context_data(**kwargs)

    # Init
    context['start'] = True
    context['count'] = self.get_queryset().count()
    context['outcomes'] = Outcome.objects.order_by('text')
    context['programs'] = Program.objects.none()
    context['eligibilities'] = Eligibility.objects.none()
    context['features'] = Feature.objects.none()
    context['services'] = Facility.objects.none()

    out_filter = self.request.GET.getlist('o')

    # >>> From OUTCOMEs let's get PROGRAMs and ELIGIBILITIEs
    outcomes = Outcome.objects.all();
    print outcomes

    if out_filter and out_filter[0]:
      context['start'] = False
      # Filter outcomes
      query = Q()
      for val in out_filter:
        query = query | Q(id=val)
      outcomes = outcomes.filter(query)

      if outcomes:
        programs = Program.objects.none();
        requirements = Eligibility.objects.none();
        features = Feature.objects.all();
        services = Facility.objects.all();
        for outcome in outcomes:
          programs = (programs | outcome.programs.all())
        programs = programs.distinct()

        query1 = Q()
        query2 = Q()
        for program in programs:
          requirements = (requirements | program.eligibility_set.all())
          for offering in program.offering_set.all():
            for val in offering.offeringfeature_set.all():
              query1 = query1 | Q(id=val.feature.id)
            for val in offering.service_delivery_site.servicedeliverysitefacility_set.all():
              query2 = query2 | Q(id=val.facility_id)

        features = features.filter(query1)
        services = services.filter(query2)

        context['features'] = features.order_by('text').distinct()
        context['services'] = services.order_by('text').distinct()
        context['programs'] = programs.order_by('name_official').distinct()
        context['eligibilities'] = requirements.order_by('text').distinct()

    return context
