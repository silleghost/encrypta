from django import template

from vault.models import Categories, Records


register = template.Library()

@register.simple_tag
def get_data_from_JSON_file(dict, key):
    if dict:
        return dict[key]


@register.simple_tag
def get_password_for_record(name):
    target_app = Records.objects.get(app_name=name)
    target_record = target_app.records
    if target_record:
        return target_record.password
    return

@register.simple_tag
def get_category_list():
    return Categories.objects.all()