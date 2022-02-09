import django_filters
from .models import Card


class CardFilter(django_filters.FilterSet):
    growth_from = django_filters.NumberFilter(field_name='growth', lookup_expr='gte')
    growth_till = django_filters.NumberFilter(field_name='growth', lookup_expr='lte')
    bust_from = django_filters.NumberFilter(field_name='bust', lookup_expr='gte')
    bust_till = django_filters.NumberFilter(field_name='bust', lookup_expr='lte')

    class Meta:
        model = Card
        fields = ['norm']