import urllib
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    queryelems = []

    # QueryDict    
    dico = context['request'].GET
    if dico.getlist('program'):
      for item in dico.getlist('program'):
        queryelems.append("program=" + str(item))

    if dico.getlist('e'):
      for item in dico.getlist('e'):
        queryelems.append("e=" + str(item))

    if dico.getlist('s'):
      for item in dico.getlist('s'):
        queryelems.append("s=" + str(item))                

    if dico.getlist('f'):
      for item in dico.getlist('f'):
        queryelems.append("f=" + str(item))   

    if dico.getlist('o'):
      for item in dico.getlist('o'):
        queryelems.append("o=" + str(item))                                

    if 'page' in kwargs:
      queryelems.append("page=" + str(kwargs['page']))        

    query = '&'.join(queryelems)
    print '+++ QUERY:', query
    return query