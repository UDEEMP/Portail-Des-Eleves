from django import template
from availableClassrooms.views import OrderedDict
register = template.Library()

@register.filter
def getValue(value, arg):
    return value[arg]
