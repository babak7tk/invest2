from datetime import datetime
import jdatetime
from django import template

register = template.Library()


@register.filter(name='addclass')
def add_classes(value, arg):
    '''
    Add provided classes to form field
    :param value: form field
    :param arg: string of classes seperated by ' '
    :return: edited field
    '''
    css_classes = value.field.widget.attrs.get('class', '')
    # check if class is set or empty and split its content to list (or init list)
    if css_classes:
        css_classes = css_classes.split(' ')
    else:
        css_classes = []
    # prepare new classes to list
    args = arg.split(' ')
    for a in args:
        if a not in css_classes:
            css_classes.append(a)
    # join back to single string
    return value.as_widget(attrs={'class': ' '.join(css_classes)})


@register.filter(name='addplaceholder')
def add_placeholder(value, placeholder):
    value.field.widget.attrs['placeholder'] = placeholder
    # join back to single string
    return value


@register.filter
def is_last_item(page_obj, items):
    result = page_obj.end_index() - page_obj.paginator.count
    if result == 0 and len(items) - 1 == 0:
        return 'yes'
    return 'no'


@register.filter
def persian_int(string):
    persianize = dict(zip("0123456789", '۰۱۲۳۴۵۶۷۸۹'))
    return ''.join(persianize[digit] if digit in persianize else digit for digit in str(string))


@register.filter(name='get_request_GET_value')
def get_request_GET_value(value, arg):
    """ value will be request.GET and arg is variable to fetch it's value. """
    try:
        return value[arg]
    except:
        return ''


@register.filter("georgian_jdate", is_safe=False)
def jdatetime_from_georgian_beautify_filter(value, arg=None):
    try:
        if arg:
            try:
                return value.strftime(arg)
            except:
                pass
        return jdatetime.datetime.fromgregorian(datetime=datetime.strptime(value, '%Y-%m-%d')).strftime('%H:%M %Y/%m/%d')
    except:
        try:
            return jdatetime.datetime.strptime(str(value), '%Y/%m/%d %H:%M:%S')
        except (ValueError, TypeError):
            return ''


@register.filter("jdate", is_safe=False)
def jdatetime_beautify_filter(value, arg=None):
    try:
        if arg:
            try:
                return value.strftime(arg)
            except:
                pass
        return value.strftime("%H:%M, %Y/%m/%d")
    except:
        try:
            return jdatetime.datetime.strptime(str(value), '%Y/%m/%d %H:%M:%S')
        except (ValueError, TypeError):
            return ''


@register.filter("get_date_from_string", is_safe=False)
def gourgian_date_filter(value, arg=None):
    try:
        return value[0:10]
    except:
        return value
