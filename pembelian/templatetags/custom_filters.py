# pembelian/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """
    Mengalikan dua nilai (value * arg) dalam template Django.
    Contoh penggunaan: {{ jumlah|mul:harga }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
