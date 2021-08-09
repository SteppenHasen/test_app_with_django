from django import template

register = template.Library()

@register.simple_tag
def custom_tag(id, some_id):
    return '{"%s": [%s]}'%(id, some_id)