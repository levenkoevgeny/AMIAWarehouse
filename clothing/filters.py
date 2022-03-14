import django_filters
from .models import Card, Employee, Clothes, Subdivision, Rank, Norm, Position, Dimensions, CapDimensions, \
    ShoesDimensions, Group, Course, EMPLOYEE_KIND


class CardFilter(django_filters.FilterSet):
    card_number = django_filters.CharFilter(field_name='card_number', lookup_expr='exact')
    last_name = django_filters.CharFilter(field_name='employee__last_name', lookup_expr='icontains')
    kind = django_filters.MultipleChoiceFilter(field_name='employee__kind', choices=EMPLOYEE_KIND)
    subdivision = django_filters.ModelMultipleChoiceFilter(field_name='employee__subdivision',
                                                           queryset=Subdivision.objects.all())
    group = django_filters.ModelMultipleChoiceFilter(field_name='employee__group',
                                                     queryset=Group.objects.all())
    course = django_filters.ModelMultipleChoiceFilter(field_name='employee__group__course',
                                                      queryset=Course.objects.all())
    rank = django_filters.ModelMultipleChoiceFilter(field_name='employee__rank',
                                                    queryset=Rank.objects.all())
    position = django_filters.ModelMultipleChoiceFilter(field_name='employee__position',
                                                        queryset=Position.objects.all())
    growth_from = django_filters.NumberFilter(field_name='growth', lookup_expr='gte')
    growth_till = django_filters.NumberFilter(field_name='growth', lookup_expr='lte')
    bust_from = django_filters.NumberFilter(field_name='bust', lookup_expr='gte')
    bust_till = django_filters.NumberFilter(field_name='bust', lookup_expr='lte')
    jacket = django_filters.ModelMultipleChoiceFilter(field_name='jacket',
                                                      queryset=Dimensions.objects.all())
    shoes = django_filters.ModelMultipleChoiceFilter(field_name='shoes',
                                                     queryset=ShoesDimensions.objects.all())
    cap = django_filters.ModelMultipleChoiceFilter(field_name='cap',
                                                   queryset=CapDimensions.objects.all())
    collar = django_filters.ModelMultipleChoiceFilter(field_name='collar',
                                                      queryset=Dimensions.objects.all())

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
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_till = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    has_to_be_deposited = django_filters.BooleanFilter(field_name='has_to_be_deposited')

    class Meta:
        model = Clothes
        fields = ['nomenclature']


class NormFilter(django_filters.FilterSet):
    class Meta:
        model = Norm
        fields = {
            'norm_title': ['icontains'],
        }
