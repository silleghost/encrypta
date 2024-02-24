from django import template
from django.core.cache import cache

from vault.models import Categories, Records


register = template.Library()


@register.simple_tag
def get_data_from_JSON_file(dict, key):
    if dict:
        return dict[key]


@register.simple_tag
def get_password_for_record(id, user):
    target_app = Records.objects.filter(user=user).get(id=id)
    return target_app.password


# @register.simple_tag
# def get_category_list_for_current_user(user):
#     return Categories.objects.filter(user=user)

@register.simple_tag
def get_category_list_for_current_user(user):
   cache_key = f"category_list_{user.id}"
   cached_data = cache.get(cache_key)
   if cached_data:
       return cached_data
   else:
       categories = Categories.objects.filter(user=user)
       cache.set(cache_key, categories)
       return categories