from django import template
from typing import Union, List, Dict
import json

register = template.Library()

@register.simple_tag
def to_json(value: Union[List, Dict]):
    return json.dumps(value)