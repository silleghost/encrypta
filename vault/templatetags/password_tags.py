from django import template

register = template.Library()

@register.simple_tag
def get_data_from_JSON_file(dict, key):
    return dict[key]