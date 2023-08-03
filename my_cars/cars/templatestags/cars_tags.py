from django import template
from cars.models import Mark

register = template.Library()

@register.simple_tag()
def get_marks():
    return Mark.objects.all()
