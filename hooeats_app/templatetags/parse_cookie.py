from django import template
import json

register = template.Library()

@register.simple_tag
def get_cookie_value(cookie_str: str, key: str):
    cookie_dict = json.loads(cookie_str)
    return cookie_dict[key]