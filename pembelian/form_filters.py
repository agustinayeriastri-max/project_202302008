from django import template

register = template.Library()

@register.filter
def kalikan(value, arg):
    try:
        return float(value) * float(arg)
    except:
        return 0
