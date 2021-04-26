# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/
# https://dev.to/nyamador/simple-custom-template-filter-in-django-3inp

from django import template

register = template.Library()

# https://stackoverflow.com/a/29794982/11528872
@register.filter 
def index(sequence, position):
    return sequence[position]