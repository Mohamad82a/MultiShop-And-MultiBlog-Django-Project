from django import template
from persiantools.jdatetime import JalaliDate

register = template.Library()

@register.filter
def to_persian_date(value):
    if value:
        # return JalaliDate(value).strftime('%d %B %Y')
        return JalaliDate(value).strftime('%Y/%m/%d')
    return ''
