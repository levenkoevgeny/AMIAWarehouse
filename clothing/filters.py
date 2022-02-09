import django_filters
from .models import Card, Employee, Clothes, Subdivision, Rank, Norm, Position


class CardFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(field_name='employee__last_name', lookup_expr='icontains')
    subdivision = django_filters.ModelMultipleChoiceFilter(field_name='employee__subdivision',
                                                           queryset=Subdivision.objects.all())
    rank = django_filters.ModelMultipleChoiceFilter(field_name='employee__rank',
                                                    queryset=Rank.objects.all())
    position = django_filters.ModelMultipleChoiceFilter(field_name='employee__position',
                                                        queryset=Position.objects.all())
    growth_from = django_filters.NumberFilter(field_name='growth', lookup_expr='gte')
    growth_till = django_filters.NumberFilter(field_name='growth', lookup_expr='lte')
    bust_from = django_filters.NumberFilter(field_name='bust', lookup_expr='gte')
    bust_till = django_filters.NumberFilter(field_name='bust', lookup_expr='lte')

    class Meta:
        model = Card
        fields = ['norm']


class EmployeeFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    subdivision = django_filters.ModelMultipleChoiceFilter(field_name='subdivision', queryset=Subdivision.objects.all())
    rank = django_filters.ModelMultipleChoiceFilter(field_name='rank', queryset=Rank.objects.all())

    class Meta:
        model = Employee
        fields = ['sex', 'kind']


class ClothesFilter(django_filters.FilterSet):
    clothes_title = django_filters.CharFilter(field_name='clothes_title', lookup_expr='icontains')
    nomenclature = django_filters.CharFilter(field_name='nomenclature', lookup_expr='icontains')
    wear_time_from = django_filters.NumberFilter(field_name='wear_time', lookup_expr='gte')
    wear_time_till = django_filters.NumberFilter(field_name='wear_time', lookup_expr='lte')

    class Meta:
        model = Clothes
        fields = ['nomenclature']


class NormFilter(django_filters.FilterSet):
    class Meta:
        model = Norm
        fields = {
            'norm_title': ['icontains'],
        }
