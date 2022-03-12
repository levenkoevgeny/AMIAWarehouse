import random

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.urls import reverse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator

from datetime import datetime, date
from dateutil.relativedelta import *
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Card, Clothes, Norm, ClothesInCard, Employee, ClothesInNorm, Subdivision, Position, Rank, SEX, \
    EMPLOYEE_KIND, Dimensions, ShoesDimensions, CapDimensions
from .forms import CardForm, ClothesForm, EmployeeForm, NormForm, ClothesInNormForm
from .serializers import ClothesInCardSerializer, CardSerializer, NormSerializer, ClothesSerializer, EmployeeSerializer, \
    ClothesInNormSerializer
from .filters import CardFilter, EmployeeFilter, ClothesFilter, NormFilter
from django_filters.rest_framework import DjangoFilterBackend


def card_list(request):
    f = CardFilter(request.GET, queryset=Card.objects.all())
    paginator = Paginator(f.qs, 50)
    page = request.GET.get('page')
    cards_list = paginator.get_page(page)
    card_form = CardForm()
    return render(request, 'clothing/card/card_list.html',
                  {'list': cards_list, 'card_form': card_form, 'filter': f})


def card_input(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('clothing:card_list'))
        else:
            return render(request, 'clothing/card/card_input_form.html', {'form': form})
    else:
        form = CardForm()
        return render(request, 'clothing/card/card_input_form.html', {'form': form})


def card_update(request, card_id):
    if request.method == 'POST':
        obj = get_object_or_404(Card, pk=card_id)
        form = CardForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('clothing:get_card', kwargs={'card_id': card_id}))
    else:
        pass


def get_card(request, card_id):
    if request.method == 'POST':
        pass
    else:
        # for update
        card = get_object_or_404(Card, pk=card_id)
        card_form = CardForm(instance=card)
        employee = card.employee
        employee_form = EmployeeForm(instance=employee)

        # norm list
        norm_clothes_list = ClothesInNorm.objects.filter(norm_id=card.norm.id).order_by('clothes__clothes_title')

        # list_of_issues = ClothesInCard.objects.filter(card_id=card_id).order_by('clothes__clothes_title')
        # list_of_clothes_id = []
        # result_list = []

        # year_list = [i + date.today().year for i in range(0, 8)]
        year_list_ = [i for i in range(date.today().year - 7, date.today().year + 1)]

        # for item in list_of_issues:
        #     list_of_clothes_id.append(item.clothes.id)

        # for cl_id in set(list_of_clothes_id):
        #     cl = get_object_or_404(Clothes, pk=cl_id)
        #     dict_cl = model_to_dict(cl)
        #     last_date = list_of_issues.filter(clothes_id=cl_id).order_by('-date_of_issue').first().date_of_issue
        #
        #     dict_cl['last_date'] = last_date
        #
        #     date_of_ending = last_date + relativedelta(months=cl.wear_time)
        #
        #     first_day_current_year = date(date.today().year, 1, 1)
        #
        #     if date_of_ending < first_day_current_year:
        #         date_of_ending = first_day_current_year
        #
        #     dict_cl['date_of_ending'] = date_of_ending
        #     dict_cl['year_of_ending'] = date_of_ending.year
        #     dict_cl['wear_time_year'] = int(dict_cl['wear_time'] / 12)
        #     result_list.append(dict_cl)

        # return render(request, 'clothing/card/card.html',
        #               {'card_form': card_form, 'employee_form': employee_form, 'card': card,
        #                'employee': employee,
        #                'norm_clothes_list': norm_clothes_list,
        #                'result_list': sorted(result_list, key=lambda d: d['clothes_title']),
        #                'year_list': year_list, 'clothes_list': Clothes.objects.all()})

        clothes_in_card_list = ClothesInCard.objects.filter(card=card)

        certificate_number = clothes_in_card_list.filter(has_certificate=True).order_by(
            '-date_of_issue').first().certificate_number

        return render(request, 'clothing/card/card.html',
                      {'card_form': card_form, 'employee_form': employee_form, 'card': card, 'employee': employee,
                       'year_list': year_list_, 'year_list_count': len(year_list_),
                       'clothes_list': Clothes.objects.all(), 'norm_clothes_list': norm_clothes_list,
                       'clothes_in_card_list': clothes_in_card_list, 'certificate_number': certificate_number
                       })


def get_card_full(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    clothes_list = ClothesInCard.objects.filter(card_id=card_id)
    clothes_list_full = Clothes.objects.all()
    list_of_clothes_id = list(set([item.clothes.id for item in clothes_list]))
    return render(request, 'clothing/card/card_full.html',
                  {'card': card,
                   'clothes_list': clothes_list,
                   'clothes_list_full': clothes_list_full,
                   'list_of_clothes_id': list_of_clothes_id})


def card_delete(request):
    pass


def clothes_list(request):
    f = ClothesFilter(request.GET, queryset=Clothes.objects.all())
    paginator = Paginator(f.qs, 30)
    page = request.GET.get('page')
    cl_list = paginator.get_page(page)
    clothes_form = ClothesForm()
    return render(request, 'clothing/clothes/clothes_list.html',
                  {'list': cl_list, 'clothes_form': clothes_form, 'filter': f})


def clothes_input(request):
    pass


def clothes_update(request, clothes_id):
    if request.method == 'POST':
        obj = get_object_or_404(Clothes, pk=clothes_id)
        form = ClothesForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('clothing:clothes_list'))
        else:
            raise Exception("Ошибка записи")
    else:
        pass


def clothes_delete(request):
    pass


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
                   'filter': f})


def employee_input(request):
    pass


def employee_update(request, employee_id, card_id):
    if request.method == 'POST':
        obj = get_object_or_404(Employee, pk=employee_id)
        form = EmployeeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('clothing:get_card', kwargs={'card_id': card_id}))
        else:
            raise Exception("Ошибка employee update data")
    else:
        pass


def norm_list(request):
    f = NormFilter(request.GET, queryset=Norm.objects.all())
    paginator = Paginator(f.qs, 30)
    page = request.GET.get('page')
    norms_list = paginator.get_page(page)
    norm_form = NormForm()
    return render(request, 'clothing/norms/norm_list.html',
                  {'list': norms_list, 'norm_form': norm_form, 'filter': f})


def norm_items(request, norm_id):
    norm = get_object_or_404(Norm, pk=norm_id)
    item_list = ClothesInNorm.objects.filter(norm_id=norm_id).order_by('clothes__clothes_title')
    clothes_in_norm_form = ClothesInNormForm()
    return render(request, 'clothing/norms/norm_items.html', {
        'norm': norm,
        'clothes_in_norm_form': clothes_in_norm_form,
        'item_list': item_list,
        'clothes_list': Clothes.objects.all(),
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
            rank=get_object_or_404(Rank, pk=random.randint(1, 11))
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


# reports
def get_sheet(request):
    # все вещи
    clothes_list = Clothes.objects.all()
    # результат
    result_dict = {}

    lll = 0

    for card in Card.objects.all():
        # норма сотрудника
        current_norm = card.norm.clothes_list.all()
        t = card.norm.id
        # вещи, которые положены сотруднику
        employee_clothes_dict = {}

        # дата начала диапазона
        date_start = date(2022, 7, 1)
        # дата окончания диапазона
        date_end = date(2022, 12, 31)
        # текущая дата
        current_date = datetime.now()

        for clothes in clothes_list:
            if clothes in current_norm:
                # список выдач этой вещи этому сотруднику
                list_of_issues = ClothesInCard.objects.filter(card_id=card.id, clothes_id=clothes.id).order_by(
                    'date_of_issue')
                norm_count = ClothesInNorm.objects.filter(norm=card.norm, clothes=clothes).first().norm_count

                if not list_of_issues:
                    employee_clothes_dict[clothes.id] = norm_count
                else:
                    date_period_start = current_date.year - clothes.wear_time / 12
                    id_need_to_delete_array = []

                    i = 0
                    while i < list_of_issues.count():
                        item = list_of_issues[i]

                        end_period_year = item.date_of_issue.year + clothes.wear_time / 12 - 1

                        if item.date_of_issue.year <= date_period_start:
                            need_to_delete_list = list_of_issues.filter(
                                date_of_issue__year__gte=item.date_of_issue.year,
                                date_of_issue__year__lte=end_period_year)
                            for date_in_list in need_to_delete_list:
                                id_need_to_delete_array.append(date_in_list.id)
                            i += need_to_delete_list.count()
                        else:
                            break

                    result_list_of_issues = list_of_issues.exclude(id__in=[*id_need_to_delete_array])

                    if result_list_of_issues.count() == 0:
                        employee_clothes_dict[clothes.id] = norm_count
                    else:
                        first_issue = result_list_of_issues.first()
                        first_issue_date_of_end = first_issue.date_of_issue + relativedelta(months=clothes.wear_time)
                        last_issue = result_list_of_issues.last()
                        last_issue_date_of_end = last_issue.date_of_issue + relativedelta(
                            months=clothes.wear_time / norm_count)
                        if first_issue_date_of_end >= date_start and first_issue_date_of_end <= date_end:
                            employee_clothes_dict[clothes.id] = norm_count
                        elif last_issue_date_of_end < date_start or last_issue_date_of_end >= date_start and first_issue_date_of_end <= date_end:
                            counter = 0
                            for item in result_list_of_issues:
                                counter = counter + item.count
                            employee_clothes_dict[clothes.id] = norm_count - counter
                        else:
                            employee_clothes_dict[clothes.id] = ""

            else:
                employee_clothes_dict[clothes.id] = ""
        result_dict[card.id] = employee_clothes_dict

    return render(request, 'clothing/reports/sheet.html',
                  {'clothes_list': clothes_list, 'card_list': Card.objects.all(), 'result_dict': result_dict})


# REST
class ClothesInCardViewSet(viewsets.ModelViewSet):
    queryset = ClothesInCard.objects.all()
    serializer_class = ClothesInCardSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class NormViewSet(viewsets.ModelViewSet):
    queryset = Norm.objects.all()
    serializer_class = NormSerializer


class ClothesViewSet(viewsets.ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class ClothesInNormViewSet(viewsets.ModelViewSet):
    queryset = ClothesInNorm.objects.all()
    serializer_class = ClothesInNormSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['norm']


# rest api endpoint for making clones based on parent
@api_view(['POST'])
def make_cloned_norm(request):
    if 'parent_norm' in request.data:
        if request.method == 'POST':
            serializer = NormSerializer(data=request.data)
            if serializer.is_valid():
                new_norm = serializer.save()
                clothes_in_norm_list = ClothesInNorm.objects.filter(norm_id=request.data['parent_norm'])
                for clothes_item in clothes_in_norm_list:
                    ClothesInNorm.objects.create(norm=new_norm, clothes=clothes_item.clothes,
                                                 norm_count=clothes_item.norm_count)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': '400 bad request'}, status=status.HTTP_400_BAD_REQUEST)
