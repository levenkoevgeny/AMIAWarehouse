import random

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
# from django.db import transaction
from django.urls import reverse
# from django.forms.models import model_to_dict
from django.core.paginator import Paginator
#
from datetime import datetime, date
# from dateutil.relativedelta import *
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Card, Clothes, Movement, NormItem, Norm, Subdivision, Position, Rank, NormItemsInNorm, Course, \
    Group, Employee, Decree, DescriptionItem, EMPLOYEE_KIND, SEX, Dimensions, CapDimensions, ShoesDimensions
from .forms import CardForm, EmployeeForm, DecreeForm, ClothesForm, NormItemForm, NormForm, NormItemsInNormForm
from .serializers import ClothesSerializer, NormItemSerializer, NormSerializer, NormItemsInNormSerializer, \
    EmployeeSerializer, DecreeSerializer, CardSerializer, MovementSerializer, DescriptionItemSerializer
from .filters import CardFilter, ClothesFilter, NormItemFilter, NormFilter, EmployeeFilter

from django_filters.rest_framework import DjangoFilterBackend


# from itertools import groupby

def card_list(request):
    request.session['back_path_card_list'] = '/clothing/cards?' + request.META.get('QUERY_STRING')
    f = CardFilter(request.GET, queryset=Card.objects.all())
    paginator = Paginator(f.qs, 50)
    page = request.GET.get('page')
    cards_list = paginator.get_page(page)
    card_form = CardForm()
    return render(request, 'clothing/card/card_list.html',
                  {'list': cards_list, 'card_form': card_form, 'filter': f})


def get_card(request, card_id):
    if request.method == 'POST':
        pass
    else:
        card = get_object_or_404(Card, pk=card_id)
        card_form = CardForm(instance=card)
        employee = card.employee
        employee_form = EmployeeForm(instance=employee)
        year_list_ = [i for i in range(date.today().year - 7, date.today().year + 1)]
        items_in_norm = card.norm.items_list.all()
        clothes_list = Clothes.objects.all()
        clothes_in_norm = clothes_list.filter(normitem__norm=card.norm)
        movement_list = Movement.objects.filter(card=card)
        movement_list_from_certificate = movement_list.filter(has_certificate=True)
        description_list = DescriptionItem.objects.filter(movement__card=card)
        if movement_list.filter(has_certificate=True).first():
            certificate_number = movement_list.filter(has_certificate=True).first().certificate_number
        else:
            certificate_number = None
        return render(request, 'clothing/card/card.html',
                      {
                          'year_list': year_list_,
                          'year_list_count': len(year_list_),
                          'items_in_norm': items_in_norm,
                          'movement_list': movement_list,
                          'movement_list_from_certificate': movement_list_from_certificate,
                          'clothes_list': clothes_list,
                          'clothes_in_norm_list': clothes_in_norm,
                          'card': card,
                          'employee': employee,
                          'employee_form': employee_form,
                          'card_form': card_form,
                          'description_list': description_list,
                          'items_in_norm_all': NormItem.objects.all(),
                          'back_path': request.session.get('back_path_card_list', '/clothing/cards'),
                          'certificate_number': certificate_number,
                      })


# def get_card_full(request, card_id):
#     card = get_object_or_404(Card, pk=card_id)
#     clothes_list = ClothesInCard.objects.filter(card_id=card_id).order_by('clothes__clothes_title')
#     clothes_list_full = Clothes.objects.all()
#     list_of_clothes_id = [item.clothes.id for item, _ in groupby(clothes_list)]
#     return render(request, 'clothing/card/card_full.html',
#                   {'card': card,
#                    'clothes_list': clothes_list,
#                    'clothes_list_full': clothes_list_full,
#                    'list_of_clothes_id': list_of_clothes_id})
#
#
def clothes_list(request):
    f = ClothesFilter(request.GET, queryset=Clothes.objects.all().order_by('clothes_title'))
    paginator = Paginator(f.qs, 30)
    page = request.GET.get('page')
    cl_list = paginator.get_page(page)
    clothes_form = ClothesForm()
    return render(request, 'clothing/clothes/clothes_list.html',
                  {'list': cl_list, 'clothes_form': clothes_form, 'filter': f})


def norm_items_list(request):
    f = NormItemFilter(request.GET, queryset=NormItem.objects.all())
    paginator = Paginator(f.qs, 30)
    page = request.GET.get('page')
    n_i_list = paginator.get_page(page)
    norm_item_form = NormItemForm()
    return render(request, 'clothing/norm_items/norm_items_list.html',
                  {'list': n_i_list, 'norm_item_form': norm_item_form, 'filter': f,
                   'clothes_list': Clothes.objects.all()})


def employee_list(request):
    f = EmployeeFilter(request.GET, queryset=Employee.objects.all())
    paginator = Paginator(f.qs, 30)
    page = request.GET.get('page')
    employees_list = paginator.get_page(page)
    employee_form = EmployeeForm()
    return render(request, 'clothing/employees/employee_list.html',
                  {'list': employees_list,
                   'employee_form': employee_form,
                   'subdivision_list': Subdivision.objects.all(),
                   'rank_list': Rank.objects.all(),
                   'position_list': Position.objects.all(),
                   'kind_list': EMPLOYEE_KIND,
                   'sex_list': SEX,
                   'group_list': Group.objects.all(),
                   'filter': f})


def employee_update(request, employee_id):
    if request.method == "POST":
        employee = get_object_or_404(Employee, pk=employee_id)
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('clothing:employee_list'))
        else:
            return render(request, 'clothing/employees/employee_update_form.html',
                          {'employee': employee, 'employee_form': form})
    else:
        employee = get_object_or_404(Employee, pk=employee_id)
        employee_form = EmployeeForm(instance=employee)
        return render(request, 'clothing/employees/employee_update_form.html',
                      {'employee': employee, 'employee_form': employee_form})


def norm_list(request):
    f = NormFilter(request.GET, queryset=Norm.objects.all().order_by('norm_title'))
    paginator = Paginator(f.qs, 30)
    page = request.GET.get('page')
    norms_list = paginator.get_page(page)
    norm_form = NormForm()
    return render(request, 'clothing/norms/norm_list.html',
                  {'list': norms_list, 'norm_form': norm_form, 'filter': f})


def norm_items(request, norm_id):
    norm = get_object_or_404(Norm, pk=norm_id)

    item_list = NormItemsInNorm.objects.filter(norm_id=norm_id)
    norm_items_in_norm_form = NormItemsInNormForm()
    # clothes_in_norm_form.fields['clothes'].queryset = clothes_in_norm_form.fields['clothes'].queryset.order_by(
    #     'clothes_title')
    norm_items_all = NormItem.objects.all()
    return render(request, 'clothing/norms/norm_items.html', {
        'norm': norm,
        'norm_items_in_norm_form': norm_items_in_norm_form,
        'item_list': item_list,
        'norm_items_all': norm_items_all,
    })


def init_dimensions(request):
    Rank.objects.all().delete()
    ranks = [
        'рядовой',
        'младший',
        'сержант',
        'старшина',
        'младший лейтенант милиции',
        'лейтенант милиции',
        'старший лейтенант милиции',
        'капитан милиции',
        'майор милиции',
        'подполковник милиции',
        'полковник милиции',
    ]

    for rank in ranks:
        Rank.objects.create(rank=rank)

    Dimensions.objects.all().delete()
    for i in range(34, 65):
        for j in range(1, 8):
            Dimensions.objects.create(dimension=str(i) + "/" + str(j))

    ShoesDimensions.objects.all().delete()
    for i in range(36, 47):
        ShoesDimensions.objects.create(shoes_dimension=str(i))

    CapDimensions.objects.all().delete()
    for i in range(52, 66):
        CapDimensions.objects.create(cap_dimension=str(i))

    return HttpResponseRedirect(reverse('clothing:card_list'))


def get_random_data(request):
    Employee.objects.all().delete()
    for i in range(1, 1000):
        new_employee = Employee(
            last_name="LastName" + str(i),
            first_name="Firstname" + str(i),
            patronymic="Patronymic" + str(i),
            kind=1,
            sex=1,
            subdivision=get_object_or_404(Subdivision, pk=random.randint(1, 2)),
            position=get_object_or_404(Position, pk=random.randint(1, 2)),
            rank=get_object_or_404(Rank, pk=random.randint(2, 12))
        )
        new_employee.save()

        new_card = Card(
            employee=new_employee,
            norm=get_object_or_404(Norm, pk=1),
            growth=random.randint(170, 190),
            bust=random.randint(90, 110),
            jacket=get_object_or_404(Dimensions, pk=random.randint(1, 20)),
            shoes=get_object_or_404(ShoesDimensions, pk=random.randint(1, 8)),
            cap=get_object_or_404(CapDimensions, pk=random.randint(1, 5)),
            collar=get_object_or_404(Dimensions, pk=random.randint(1, 20)),
        )
        new_card.save()

    return HttpResponseRedirect(reverse('clothing:card_list'))


# # reports
# def get_sheet(request):
#     f = CardFilter(request.GET, queryset=Card.objects.all())
#     cards_list = f.qs
#     if request.META['QUERY_STRING']:
#         only_filter = False
#     else:
#         only_filter = True
#
#     # все вещи
#     clothes_list = Clothes.objects.all()
#     # результат
#     result_dict = {}
#
#     # for card in Card.objects.all():
#     #     # норма сотрудника
#     #     current_norm = card.norm.clothes_list.all()
#     #     t = card.norm.id
#     #     # вещи, которые положены сотруднику
#     #     employee_clothes_dict = {}
#     #
#     #     # дата начала диапазона
#     #     date_start = date(2022, 7, 1)
#     #     # дата окончания диапазона
#     #     date_end = date(2022, 12, 31)
#     #     # текущая дата
#     #     current_date = datetime.now()
#     #
#     #     for clothes in clothes_list:
#     #         if clothes in current_norm:
#     #             # список выдач этой вещи этому сотруднику
#     #             list_of_issues = ClothesInCard.objects.filter(card_id=card.id, clothes_id=clothes.id,
#     #                                                           has_replacement=False).order_by(
#     #                 'date_of_issue')
#     #             norm_count = ClothesInNorm.objects.filter(norm=card.norm, clothes=clothes).first().norm_count
#     #
#     #             if not list_of_issues:
#     #                 employee_clothes_dict[clothes.id] = norm_count
#     #             else:
#     #                 date_period_start = current_date.year - clothes.wear_time / 12
#     #                 id_need_to_delete_array = []
#     #
#     #                 i = 0
#     #                 while i < list_of_issues.count():
#     #                     item = list_of_issues[i]
#     #
#     #                     end_period_year = item.date_of_issue.year + clothes.wear_time / 12 - 1
#     #
#     #                     if item.date_of_issue.year <= date_period_start:
#     #                         need_to_delete_list = list_of_issues.filter(
#     #                             date_of_issue__year__gte=item.date_of_issue.year,
#     #                             date_of_issue__year__lte=end_period_year)
#     #                         for date_in_list in need_to_delete_list:
#     #                             id_need_to_delete_array.append(date_in_list.id)
#     #                         i += need_to_delete_list.count()
#     #                     else:
#     #                         break
#     #
#     #                 result_list_of_issues = list_of_issues.exclude(id__in=[*id_need_to_delete_array])
#     #
#     #                 if result_list_of_issues.count() == 0:
#     #                     employee_clothes_dict[clothes.id] = norm_count
#     #                 else:
#     #                     first_issue = result_list_of_issues.first()
#     #                     first_issue_date_of_end = first_issue.date_of_issue + relativedelta(months=clothes.wear_time)
#     #                     last_issue = result_list_of_issues.last()
#     #                     last_issue_date_of_end = last_issue.date_of_issue + relativedelta(
#     #                         months=clothes.wear_time / norm_count)
#     #                     if first_issue_date_of_end >= date_start and first_issue_date_of_end <= date_end:
#     #                         employee_clothes_dict[clothes.id] = norm_count
#     #                     elif last_issue_date_of_end < date_start or last_issue_date_of_end >= date_start and first_issue_date_of_end <= date_end:
#     #                         counter = 0
#     #                         for item in result_list_of_issues:
#     #                             counter = counter + item.count
#     #                         employee_clothes_dict[clothes.id] = norm_count - counter
#     #                     else:
#     #                         employee_clothes_dict[clothes.id] = ""
#     #
#     #         else:
#     #             employee_clothes_dict[clothes.id] = ""
#     #     result_dict[card.id] = employee_clothes_dict
#
#     # return render(request, 'clothing/reports/sheet.html',
#     #               {'clothes_list': clothes_list, 'card_list': Card.objects.all(), 'result_dict': result_dict})
#
#     return render(request, 'clothing/reports/sheet.html', {'only_filter': only_filter, 'filter': f})
#
#


# # REST


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class ClothesViewSet(viewsets.ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer


class NormItemViewSet(viewsets.ModelViewSet):
    queryset = NormItem.objects.all()
    serializer_class = NormItemSerializer


class NormViewSet(viewsets.ModelViewSet):
    queryset = Norm.objects.all()
    serializer_class = NormSerializer


class NormItemsInNormViewSet(viewsets.ModelViewSet):
    queryset = NormItemsInNorm.objects.all()
    serializer_class = NormItemsInNormSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['norm']


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class MovementViewSet(viewsets.ModelViewSet):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer


class DescriptionItemViewSet(viewsets.ModelViewSet):
    queryset = DescriptionItem.objects.all()
    serializer_class = DescriptionItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movement']


class DecreeViewSet(viewsets.ModelViewSet):
    queryset = Decree.objects.all()
    serializer_class = DecreeSerializer


# # rest api endpoint for making clones based on parent
@api_view(['POST'])
def make_cloned_norm(request):
    if 'parent_norm' in request.data:
        if request.method == 'POST':
            serializer = NormSerializer(data=request.data)
            if serializer.is_valid():
                new_norm = serializer.save()
                norm_items_in_norm_list = NormItemsInNorm.objects.filter(norm_id=request.data['parent_norm'])
                for norm_item in norm_items_in_norm_list:
                    NormItemsInNorm.objects.create(norm=new_norm, norm_item=norm_item.norm_item,
                                                   norm_count=norm_item.norm_count, wear_time=norm_item.wear_time)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': '400 bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def movement_several_add(request):
    if request.method == 'POST':
        serializer = MovementSerializer(data=request.data)
        if serializer.is_valid():
            movement = serializer.save()
            norm_item = get_object_or_404(NormItem, pk=request.data['norm_item'])
            for clothes in norm_item.item_clothes.all():
                new_description = DescriptionItem(movement=movement, clothes=clothes, count=request.data['count'])
                new_description.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': ''}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
