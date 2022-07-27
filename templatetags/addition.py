from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def addition(value):
    amount = 0
    if value is None:
        return amount
    else:
        for v in value:
            amount += int(float(v.amount))
        return amount
