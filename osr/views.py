# -*- coding: utf-8 -*-
import json
import codecs
import re
import os.path
from django.template import loader
from datetime import datetime
from django.views import generic
from django.db.models import Q
from django.urls import reverse
from django.utils import translation
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from easy_pdf.views import PDFTemplateView
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.utils.translation import ugettext_lazy as _
from .forms import FeedbackForm
from .models import Offering, Program, Outcome, Eligibility, Feature, Facility, ServiceDeliverySite 
from .models import ProfileSection, GlossaryEntry, Feedback
from .models import GoalPath, Recommendation, ExternalLink, UnhappyPath, FutureMatch

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
  return render(request, 'osr/intro.html', {'programs': programs})

def detail_program(request, program_code):
  """ 
  This view corresponds to the dynamic program pages.
  There is a program page for each program in the DB.
  This page will show details about each program.
  """  
  program = get_object_or_404(Program, code=program_code.upper())  
  return render(request, 'osr/program.html', {'program': program})  

def glossary(request):
  """ 
  This view corresponds to the adult learning glossary page.
  This page will show definitions of terms that are difficult for adult learners to understand.
  """

  # All glossary entries
  entries = GlossaryEntry.objects.all().order_by('key')    
  return render(request, 'osr/glossary.html', {'entries': entries})

def feedback(request):
  """ 
  This view corresponds to the feedback page.
  This page will show a survey form.
  """

  paramSuccess = False
  # If this is a POST request we need to process the form data
  if request.method == 'POST':
    # Create a form instance and populate it with data from the request
    form = FeedbackForm(request.POST)
    # Check whether it's valid
    if form.is_valid():
      feedback_record = Feedback.objects.create(
        purpose_of_visit = form.cleaned_data.get('purpose_of_visit'),
        found_what_i_was_looking_for = form.cleaned_data.get('found_what_i_was_looking_for'),
        website_easy_to_navigate = form.cleaned_data.get('website_easy_to_navigate'),
        information_easy_to_understand = form.cleaned_data.get('information_easy_to_understand'),
        matchmaker_easy_to_use = form.cleaned_data.get('matchmaker_easy_to_use'),
        matchmaker_helpful = form.cleaned_data.get('matchmaker_helpful'),
        rating = form.cleaned_data.get('rating'),
        type_of_user = form.cleaned_data.get('type_of_user'),
        most_useful_feature = form.cleaned_data.get('most_useful_feature'),
        content_or_feature_request = form.cleaned_data.get('content_or_feature_request'),
        general_comment = form.cleaned_data.get('general_comment'),
        created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      )
      paramSuccess = True
  # If a GET (or any other method) we'll create a blank form
  else:
    form = FeedbackForm()    

  return render(request, 'osr/feedback.html', {'form': form, 'paramSuccess': paramSuccess})  

def matchmaker(request):
  """ 
  This view corresponds to the matchmaker page.
  This page will present the user with a series of questions.
  """
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

  # Recommendations will be retrieved from the DB
  recommendations = ExternalLink.objects.none()

  # Variables used to display a message when the user chooses to e-mail themselves their results
  wasEmailSent = False
  emailAddress = ''

  if request.method == "GET":
    if 'wasEmailSent' in request.session and 'emailAddress' in request.session:
      wasEmailSent = True
      emailAddress = request.session['emailAddress']

    # If there are cached vars then proceed normally
    if 'curr_matches' in request.session or 'futr_matches' in request.session or \
       'link_list' in request.session or 'path_list' in request.session or 'reco_list' in request.session:
      # TODO: Do these make sense? The template could load them straight from the cache
      curr_programs, links, recos, messages = get_learner_matches_from_cache(request)
      groupOf1s, groupOf2s, groupOf3s, paramsPrograms = group_programs(curr_programs)
      profile_lines_basic, profile_lines_goals, profile_lines_needs = get_learner_profile_from_cache(request)

    # If there are no cached vars then redirect user to the matchmaker page  
    else:
      return redirect('/osr/matchmaker/')

  if request.method == "POST":
    # Create dictionary from JSON created during the matchmaker experience
    dico = json.loads(request.POST.get("dico", "").encode('utf-8'))
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    print dico
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    
    # Reset cache but reactivate current django language
    reset_cache(request) 
    translation.activate(dico['lang'])      

    # Save program matches to cache
    curr_programs, links, recos, messages = save_learner_matches_to_cache(dico, request)

    print '$$$$$$$$$$$$$$$$$$$'
    print '[C]:', curr_programs
    print '[L]:', links
    print '[R]:', recos
    print '[M]:', messages
    print '$$$$$$$$$$$$$$$$$$$'

    # Group programs
    groupOf1s, groupOf2s, groupOf3s, paramsPrograms = group_programs(curr_programs)
    # TODO:
    # Save learner profile to cache
    profile_lines_basic, profile_lines_goals, profile_lines_needs = save_learner_profile_to_cache(dico, request)

  request.session[LANGUAGE_SESSION_KEY] = translation.get_language()

  return render(request, 'osr/transition.html', 
    {'number': curr_programs.count, 'groupOf1s': groupOf1s, 'groupOf2s': groupOf2s, 'groupOf3s': groupOf3s, 
     'paramsPrograms': paramsPrograms, 'links': links, 'recos': recos, 'messages': messages,
     'proLinesBasic': profile_lines_basic, 'proLinesGoals': profile_lines_goals, 'proLinesNeeds': profile_lines_needs,
     'wasEmailSent': wasEmailSent, 'emailAddress': emailAddress})

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

  return render(request, 'osr/comparison.html', {'programs': programs})

class ResultsPDFView(PDFTemplateView):
  """ 
  This view is triggered when a user clicks the "Download PDF" button in the results page.
  It is used to create a PDF with the results of the matchmaker for a particular user.
  The info to be included in the PDF is retrieved from the cache. 
  """  
  pdf_filename = _('results.pdf')
  template_name = 'osr/print.html'  

  def get_context_data(self, **kwargs):
    context = super(ResultsPDFView, self).get_context_data(pagesize = "A4", title = _("My results"), **kwargs)

    # Retrieve information from cache
    curr_matches, links, recos, messages = get_learner_matches_from_cache(self.request)
    
    # Variables to be passed in to the HTML to render the PDF
    context['matches'] = curr_matches
    context['recos'] = recos
    context['links'] = links
    context['messages'] = messages
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
    curr_matches, links, recos, messages = get_learner_matches_from_cache(request)

    # Variables to be included in the email
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    program_base = "%s://%s%s" % (request.scheme, request.get_host(), "/osr/program")
    results_path = "%s://%s%s" % (request.scheme, request.get_host(), reverse('osr:transition'))

    # Load template of HTML message with placeholders
    curr_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(curr_path, "templates/osr/email.html")

    # Fill in placeholders in HTML message
    list_program_matches = []
    for m in curr_matches:
      program_path = '%s/%s' % (program_base, m.code.lower())
      list_program_matches.append({ 'name': m.name_official, 'description': m.description, 'path': program_path})

    list_recos = []
    for reco in recos:
      list_recos.append({ 'text': reco.text })

    list_links = []
    for link in links:
      list_links.append({ 'reason': link.reason, 'text': link.text, 'link': link.link })

    html_message = loader.render_to_string(
      file_path,
      {
        'programs': list_program_matches,
        'links':  list_links,
        'recos':  list_recos, 
        'messages':  messages, 
        'number': len(list_program_matches),
        'website': results_path,
        'timestamp': timestamp
      }
    )        

    send_mail(
      subject = _('Your results and recommendations'),
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
  codelist = []
  for program in programs:
    proglist.append(program)   
    codelist.append('p=' + program.code)
  prog_url = '?%s' % ('&'.join(codelist))
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

def get_links_from_db(link_list):
  if not link_list:
    return ExternalLink.objects.none()
  else:
    links = ExternalLink.objects.all()
    query = Q()
    for code in link_list:
      query = query | Q(code=code)
    links = links.filter(query)           
    return links

def get_paths_from_db(path_list):
  if not path_list:
    return UnhappyPath.objects.none()
  else:
    paths = UnhappyPath.objects.all()
    query = Q()
    for code in path_list:
      query = query | Q(code=code)
    paths = paths.filter(query)           
    return paths    

def get_recos_from_db(reco_list):
  if not reco_list:
    return Recommendation.objects.none()
  else:
    recos = Recommendation.objects.all()
    query = Q()
    for code in reco_list:
      query = query | Q(code=code)
    recos = recos.filter(query)           
    return recos

def get_futr_program_matches_from_db(futr_list):
  if not futr_list:
    return FutureMatch.objects.none()
  else:
    matches = FutureMatch.objects.all()
    query = Q()
    for code in futr_list:
      query = query | Q(code=code)
    matches = matches.filter(query)           
    return matches        

def get_curr_program_matches_from_db(codelist):
  if not codelist:
    return Program.objects.none()
  else:
    programs = Program.objects.all()
    query = Q()
    for code in codelist:
      query = query | Q(code=code)
    programs = programs.filter(query)   
    return programs

###########################################################################################
#####                                      TODO                                       #####
###########################################################################################

def get_learner_matches_from_cache(request):
  # (Current program matches, Links, Recos, Messages)
  return (
    get_curr_program_matches_from_db(request.session['curr_matches']), 
    get_links_from_db(request.session['link_list']),
    get_recos_from_db(request.session['reco_list']),
    format_messages(get_paths_from_db(request.session['path_list']), get_futr_program_matches_from_db(request.session['futr_matches'])))    

def save_learner_matches_to_cache(dico, request):
  curr_list, futr_list, reco_list, link_list, path_list = [], [], [], [], []
  if 'curr_matches' not in request.session and 'futr_matches' not in request.session and \
     'reco_list' not in request.session and 'link_list' not in request.session and \
     'path_list' not in request.session:

    request.session['curr_matches'] = []
    request.session['futr_matches'] = []
    request.session['reco_list'] = []
    request.session['link_list'] = []
    request.session['path_list'] = []

    for key in dico.keys():
      # Current program matches
      # Variables that represent current program matches follow the format
      # "match_curr_" + 3-letter code of the program
      if key.startswith('match_curr'):
        curr_list.append(key.split('_')[2].upper())

      # Future program matches
      # Variables that represent future program matches follow the format
      # "match_futr_" + 3-letter code of the program    
      if key.startswith('match_futr'):
        futr_list.append(key)

      # External links
      # Variables that represent external links follow the format: "link_" + name
      if key.startswith('link'):
        link_list.append(key)  

      # Recommendations
      # Variables that represent recommendations follow the format: "msg_" + name
      if key.startswith('msg'):
        reco_list.append(key) 

      # Unhappy paths
      # Variables that represent unhappy path messages follow the format: "err_" + name
      if key.startswith('err'):
        path_list.append(key)                        

    request.session['curr_matches'] = curr_list
    request.session['futr_matches'] = futr_list
    request.session['reco_list'] = reco_list
    request.session['link_list'] = link_list
    request.session['path_list'] = path_list                      

  # (Current program matches, Links, Recos, Messages)
  return (
    get_curr_program_matches_from_db(curr_list),     
    get_links_from_db(link_list),
    get_recos_from_db(reco_list),
    format_messages(get_paths_from_db(path_list), get_futr_program_matches_from_db(futr_list)))

def format_messages(paths, futr_programs):
  # Get current set of goals
  goals = []
  for path in paths:
    if path.goal not in goals:
      goals.append(path.goal)
  for prog in futr_programs:
    if prog.goal not in goals:
      goals.append(prog.goal)      
  print "### GOALS ###", goals

  # Create goal-related messages to be sent to template
  # message = { 'goal': 'X', 'future_matches': [], 'paths': [] }
  messages = []
  for goal in goals:
    message = { 'goal': goal.text, 'future_matches': [], 'paths': [] }
    for path in paths:
      if goal == path.goal:
        message['paths'].append(path.text)
    for prog in futr_programs:
      if goal == prog.goal:
        message['future_matches'].append(prog.text) 
    messages.append(message) 

  return messages

def save_learner_profile_to_cache(dico, request):
  sections = ProfileSection.objects.all()
  profile_lines_basic, profile_lines_goals, profile_lines_needs = [], [], []

  query = Q()
  print '$$$$$'
  for key in dico:
    print key
    if key.startswith('profile'):  
      query = query | Q(code=key)
  print '$$$$$'      
  sections = sections.filter(query)

  # Replace placeholders
  patObj = re.compile(r'#(.+?)#')
  for section in sections:
    text_en = section.text_en.encode('utf-8')
    text_fr = section.text_fr.encode('utf-8')

    if '%' in text_en:
      text_en = text_en.replace('%', dico[section.code].encode('utf-8'))
    if '#' in text_en:
      matches = re.findall(patObj, text_en)
      if matches:        
        for match in matches:
          text_en = text_en.replace('#%s#' % (match), dico[match].encode('utf-8'))            

    if '%' in text_fr:
      text_fr = text_fr.replace('%', dico[section.code].encode('utf-8'))
    if '#' in text_fr:      
      matches = re.findall(patObj, text_fr)
      if matches:        
        for match in matches:
          text_fr = text_fr.replace('#%s#' % (match), dico[match].encode('utf-8'))            

    if section.section == 'Information':
      profile_lines_basic.append({ 'en': text_en, 'fr': text_fr })
    if section.section == 'Goals':
      profile_lines_goals.append({ 'en': text_en, 'fr': text_fr })
    if section.section == 'Needs':
      profile_lines_needs.append({ 'en': text_en, 'fr': text_fr })  

  request.session['profile_lines_basic'] = profile_lines_basic    
  request.session['profile_lines_goals'] = profile_lines_goals
  request.session['profile_lines_needs'] = profile_lines_needs

  return (profile_lines_basic, profile_lines_goals, profile_lines_needs)

def get_learner_profile_from_cache(request):
  return (request.session['profile_lines_basic'], 
          request.session['profile_lines_goals'], 
          request.session['profile_lines_needs'])

def reset_cache(request):
  """ Delete all variables stored in the cache """
  for key in request.session.keys():
    del request.session[key]  
