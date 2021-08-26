from django import template
from django.forms.widgets import CheckboxInput
import os

register = template.Library()

@register.filter
def get( dict, key, default = '' ):
  """
  Usage: 

  view: 
  some_dict = {'keyA':'valueA','keyB':{'subKeyA':'subValueA','subKeyB':'subKeyB'},'keyC':'valueC'}
  keys = ['keyA','keyC']
  template: 
  {{ some_dict|get:"keyA" }}
  {{ some_dict|get:"keyB"|get:"subKeyA" }}
  {% for key in keys %}{{ some_dict|get:key }}{% endfor %}
  """

  try:
    return dict.get(key,default)
  except:
    return default


@register.filter
def filename(fichier):
    return os.path.basename(fichier.name)


@register.filter(name="is_checkbox")
def is_checkbox(value):
  return isinstance(value, CheckboxInput)