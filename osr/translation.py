# -*- coding: utf-8 -*-
from modeltranslation.translator import register, TranslationOptions
from .models import Program, ProgramRegistrationSteps, ProgramBestForScenarios
from .models import Outcome, Eligibility, Subject, Stream, Profession, Feature, Facility
from .models import ExternalLink, LearningOption, ScheduleOption, ProgramLinks, ImmigrationStatus
from .models import Benefit, ProfileSection, GlossaryEntry, Recommendation 
from .models import GoalPath, UnhappyPath, FutureMatch

@register(Program)
class ProgramTranslationOptions(TranslationOptions):
  fields = ('name_official', 'name_branding', 'description', 'description_for_comparison_page', 'details', 'length', 'subsidies', 'support', 'funding', 'fees', 'types_of_sps', 'map_sp_label', 'ministry', 'eligibility_disclaimer')

@register(ProgramRegistrationSteps)
class ProgramRegistrationStepsTranslationOptions(TranslationOptions):
  fields = ('text',)

@register(ProgramBestForScenarios)
class ProgramBestForScenariosTranslationOptions(TranslationOptions):
  fields = ('text',)  

@register(Outcome)
class OutcomeTranslationOptions(TranslationOptions):
  fields = ('text',)      

@register(Eligibility)
class EligibilityTranslationOptions(TranslationOptions):
  fields = ('text',)     

@register(Subject)
class SubjectTranslationOptions(TranslationOptions):
  fields = ('text',)     

@register(Stream)
class StreamTranslationOptions(TranslationOptions):
  fields = ('text',)  

@register(ExternalLink)
class ExternalLinkTranslationOptions(TranslationOptions):
  fields = ('text', 'reason')

@register(Recommendation)
class RecommendationTranslationOptions(TranslationOptions):
  fields = ('text',)

@register(GoalPath)
class GoalPathTranslationOptions(TranslationOptions):
  fields = ('text',)

@register(UnhappyPath)
class UnhappyPathTranslationOptions(TranslationOptions):
  fields = ('text',)

@register(FutureMatch)
class FutureMatchTranslationOptions(TranslationOptions):
  fields = ('text',)          

@register(ProfileSection)
class ProfileSectionTranslationOptions(TranslationOptions):
  fields = ('text',) 

@register(Profession)
class ProfessionTranslationOptions(TranslationOptions):
  fields = ('text',) 

@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
  fields = ('text',)                

@register(Facility)
class FacilityTranslationOptions(TranslationOptions):
  fields = ('text',) 

@register(LearningOption)
class LearningOptionTranslationOptions(TranslationOptions):
  fields = ('text',)

@register(ScheduleOption)
class ScheduleOptionTranslationOptions(TranslationOptions):
  fields = ('text',)  

@register(ProgramLinks)
class ProgramLinksTranslationOptions(TranslationOptions):
  fields = ('text',) 

@register(ImmigrationStatus)
class ImmigrationStatusTranslationOptions(TranslationOptions):
  fields = ('text',)      

@register(Benefit)
class BenefitTranslationOptions(TranslationOptions):
  fields = ('text',)        

@register(GlossaryEntry)
class GlossaryEntryTranslationOptions(TranslationOptions):
  fields = ('key', 'definition')  
