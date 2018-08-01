# -*- coding: utf-8 -*-
from django import forms
from .models import Feedback
from django.utils.translation import ugettext_lazy as _

class MyRadioSelect(forms.RadioSelect):
  template_name = 'osr/radio.html'  

class FeedbackForm(forms.Form):
  purpose_of_visit = forms.ChoiceField(
    widget = MyRadioSelect(
      attrs = {'style': 'margin-bottom:0.5rem; margin-top:0rem;'}      
    ), 
    choices = (
      ('learn about adult learning', _('Learn about adult learning')), 
      ('learn about a specific adult learning program', _('Learn about a specific adult learning program')),
      ('get matched to a program', _('Get matched to a program')),
      ('other', _('Other'))
    ),
    label = _("What was the purpose of your visit today?")
  )

  found_what_i_was_looking_for = forms.ChoiceField(
    widget = MyRadioSelect(
      attrs = {'style': 'margin-bottom:0.5rem; margin-top:0rem;'}      
    ), 
    choices = (
      ('yes', _('Yes')), 
      ('no', _('No'))
    ),
    label = _("Did you find what you were looking for?")
  )  

  website_easy_to_navigate = forms.ChoiceField(
    widget = MyRadioSelect(
      attrs = {'style': 'margin-bottom:0.5rem; margin-top:0rem;'}      
    ), 
    choices = (
      ('yes', _('Yes')), 
      ('no', _('No'))
    ),
    label = _("Is the adult learning website easy to navigate?")
  )  

  information_easy_to_understand = forms.ChoiceField(
    widget = MyRadioSelect(
      attrs = {'style': 'margin-bottom:0.5rem; margin-top:0rem;'}      
    ), 
    choices = (
      ('yes', _('Yes')), 
      ('no', _('No'))
    ),
    label = _("Is the information easy to understand?")
  )  

  matchmaker_easy_to_use = forms.ChoiceField(
    widget = MyRadioSelect(
      attrs = {'style': 'margin-bottom:0.5rem; margin-top:0rem;'}      
    ), 
    choices = (
      ('yes', _('Yes')), 
      ('no', _('No'))
    ),
    label = _('If you used the matchmaker, was it easy to use?')
  )  

  matchmaker_helpful = forms.ChoiceField(
    widget = MyRadioSelect(
      attrs = {'style': 'margin-bottom:0.5rem; margin-top:0rem;'}      
    ), 
    choices = (
      ('yes', _('Yes')), 
      ('no', _('No'))
    ),
    label = _("If you used the matchmaker, did it help you find a program?")
  )  

  rating = forms.ChoiceField(
    widget = MyRadioSelect(
      attrs = {'style': 'margin-bottom:0.5rem; margin-top:0rem;'}      
    ), 
    choices = (
      ('very satisfied', _('Very satisfied')), 
      ('satisfied', _('Satisfied')),
      ('neutral', _('Neutral or no opinion')),
      ('unsatisfied', _('Unsatisfied')),
      ('very unsatisfied', _('Very unsatisfied')),
    ),
    label = _("Please rate the overall experience you had with the adult learning website")
  )  

  type_of_user = forms.ChoiceField(
    widget = MyRadioSelect(
      attrs = {'style': 'margin-bottom:0.5rem; margin-top:0rem;'}      
    ), 
    choices = (
      ('prospective learner', _('Prospective learner')), 
      ('current learner', _('Current learner')),
      ('instructor', _('Instructor')),
      ('service provider', _('Service provider')),
      ('caseworker', _('Caseworker')),
      ('counsellor', _('Counsellor')),
      ('other', 'Other')
    ),
    label = _("You are visiting the adult learning website as a:")
  )  

  most_useful_feature = forms.ChoiceField(
    widget = MyRadioSelect(
      attrs = {'style': 'margin-bottom:0.5rem; margin-top:0rem;'}      
    ), 
    choices = (
      ('comparison table', _('Comparison table')), 
      ('matchmaker', _('Matchmaker')),
      ('program page', _('Program page')),
      ('live chat', _('Live chat')),
      ('other', _('Other'))
    ),
    label = _("What feature helped you find a program?")
  )                

  content_or_feature_request = forms.CharField(
    max_length = 2000,
    widget = forms.Textarea(
      attrs = {
        'placeholder': _('Write your comment here...')
      }
    ),
    label = _("What other information or feature would make this website more useful for you?")
  )  

  general_comment = forms.CharField(
    max_length = 2000,
    widget = forms.Textarea(
      attrs = {
        'placeholder': _('Write your comment here...')
      }
    ),
    label = _("Share any comment you have about the adult learning website")
  )  

  def clean(self):
    cleaned_data = super(FeedbackForm, self).clean()
    col01 = cleaned_data.get('purpose_of_visit')
    col02 = cleaned_data.get('found_what_i_was_looking_for')
    col03 = cleaned_data.get('website_easy_to_navigate')
    col04 = cleaned_data.get('information_easy_to_understand')
    col05 = cleaned_data.get('matchmaker_easy_to_use')
    col06 = cleaned_data.get('matchmaker_helpful')    
    col07 = cleaned_data.get('rating')
    col08 = cleaned_data.get('type_of_user')
    col09 = cleaned_data.get('most_useful_feature')    
    col10 = cleaned_data.get('content_or_feature_request')
    col11 = cleaned_data.get('general_comment')        
    if not col01 or not col02 or not col03 or not col04 or not col05 or not col06 \
      or not col07 or not col08 or not col09 or not col10 or not col11:
      raise forms.ValidationError(_('Please correct the errors in this form and submit it again.'))