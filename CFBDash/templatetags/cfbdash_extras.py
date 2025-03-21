import re
from django import template

register = template.Library()

@register.filter
def convert_camel(value):
    spaced = re.sub(r'(?<!^)(?=[A-Z])', ' ', value)
    return spaced.title()