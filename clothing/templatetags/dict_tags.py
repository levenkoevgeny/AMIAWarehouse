from django import template
from django.template.defaultfilters import floatformat

from clothing.models import Clothes
from django.shortcuts import get_object_or_404
from django.db.models.functions import Lower

register = template.Library()


@register.filter(name='get_sub_dict')
def get_sub_dict(value, index):
    return value[index]


@register.filter(name='get_issues_dates')
def get_issues_dates(value, clothes_id):
    return value.filter(clothes__id=clothes_id).order_by('date_of_issue')


@register.filter(name='get_clothes')
def get_clothes(value, clothes_id):
    return get_object_or_404(Clothes, pk=clothes_id)


@register.filter(name='sort_by')
def sort_by(queryset, order):
    return queryset.order_by(Lower(order))


@register.filter(name='formatted_float')
def formatted_float(value):
    value = floatformat(value, arg=2)
    return str(value).replace(',', '.')

