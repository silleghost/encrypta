from django import template

from vault.models import Categories, Records


register = template.Library()

@register.simple_tag
def get_data_from_JSON_file(dict, key):
    if dict:
        return dict[key]


@register.simple_tag
def get_password_for_record(name, user):
    target_app = Records.objects.filter(user=user).get(app_name=name)
    return target_app.password


@register.simple_tag
def get_category_list_for_current_user(user):
    return Categories.objects.filter(user=user)