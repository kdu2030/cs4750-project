from django import template
from typing import Union, List, Dict
import json

register = template.Library()

@register.simple_tag
def to_json(value: Union[List, Dict]):
    return json.dumps(value)

@register.simple_tag
def inc_day_of_week(value: int):
    day_value = value + 1
    if day_value == 7:
        day_value = 0
    return day_value