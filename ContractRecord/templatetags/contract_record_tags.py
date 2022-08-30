from datetime import datetime
import jdatetime
from django import template

register = template.Library()


@register.filter("user_phone_format", is_safe=False)
def user_phone_format(value, arg=None):
    try:
        return value[1:]
    except:
        return value
