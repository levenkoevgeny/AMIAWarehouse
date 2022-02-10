from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.urls import reverse
from django.forms.models import model_to_dict
from django.forms import modelformset_factory

from datetime import datetime, date
from dateutil.relativedelta import *
from rest_framework import viewsets

from .models import Card, Clothes, Norm, ClothesInCard, Employee, ClothesInNorm, Subdivision, Position, Rank, SEX, \
    EMPLOYEE_KIND
from .forms import CardForm, ClothesForm, EmployeeForm, NormForm, ClothesInNormForm
from .serializers import ClothesInCardSerializer, CardSerializer, NormSerializer, ClothesSerializer, EmployeeSerializer, \
    ClothesInNormSerializer
from .filters import CardFilter, EmployeeFilter, ClothesFilter, NormFilter


def card_list(request):
    f = CardFilter(request.GET, queryset=Card.objects.all())
    card_list = f.qs
    card_form = CardForm()
    return render(request, 'clothing/card/card_list.html',
                  {'card_list': card_list, 'card_form': card_form, 'filter': f})


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
        norm_clothes_list = ClothesInNorm.objects.filter(norm_id=card.norm.id)

        list_of_issues = ClothesInCard.objects.filter(card_id=card_id)
        list_of_clothes_id = []
        result_list = []

        year_list = [i + date.today().year for i in range(0, 8)]

        for item in list_of_issues:
            list_of_clothes_id.append(item.clothes.id)
        for cl_id in set(list_of_clothes_id):
            cl = get_object_or_404(Clothes, pk=cl_id)
            dict_cl = model_to_dict(cl)
            last_date = list_of_issues.filter(clothes_id=cl_id).order_by('-date_of_issue').first().date_of_issue
            dict_cl['last_date'] = last_date
            date_of_ending = last_date + relativedelta(months=cl.wear_time)
            dict_cl['date_of_ending'] = date_of_ending
            dict_cl['year_of_ending'] = date_of_ending.year
            result_list.append(dict_cl)

        return render(request, 'clothing/card/card.html',
                      {'card_form': card_form, 'employee_form': employee_form, 'card': card,
                       'employee': employee,
                       'norm_clothes_list': norm_clothes_list, 'result_list': result_list,
                       'year_list': year_list, 'clothes_list': Clothes.objects.all()})


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
    clothes_list = f.qs
    clothes_form = ClothesForm()
    return render(request, 'clothing/clothes/clothes_list.html',
                  {'clothes_list': clothes_list, 'clothes_form': clothes_form, 'filter': f})


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
    employee_list = f.qs
    employee_form = EmployeeForm()
    return render(request, 'clothing/employees/employee_list.html',
                  {'employee_list': employee_list,
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
    norm_list = f.qs
    norm_form = NormForm()
    return render(request, 'clothing/norms/norm_list.html',
                  {'norm_list': norm_list, 'norm_form': norm_form, 'filter': f})


def norm_items(request, norm_id):
    norm = get_object_or_404(Norm, pk=norm_id)
    item_list = ClothesInNorm.objects.filter(norm_id=norm_id).order_by('clothes')
    clothes_in_norm_form = ClothesInNormForm()
    return render(request, 'clothing/norms/norm_items.html', {
        'norm': norm,
        'clothes_in_norm_form': clothes_in_norm_form,
        'item_list': item_list,
        'clothes_list': Clothes.objects.all(),
    })


import random

def get_random_data(request):
    for i in range(1, 2000):
        new_employee = Employee(
            last_name="LastName" + str(i),
            first_name="Firstname" + str(i),
            patronymic="Patronymic" + str(i),
            kind=1,
            sex=1,
            subdivision=get_object_or_404(Subdivision, pk=1),
            position=get_object_or_404(Position, pk=1)
        )
        new_employee.save()

        new_card = Card(
            employee=new_employee,
            norm=get_object_or_404(Norm, pk=1),
            growth=random.randint(170, 190),
            bust=random.randint(90, 110),
            jacket=random.randint(1, 2),
            shoes=random.randint(1, 2),
            cap=random.randint(55, 60),
            collar=random.randint(1, 2),
        )
        new_card.save()


# reports
def get_sheet(request):
    clothes_list = Clothes.objects.all()
    result_dict = {}
    for card in Card.objects.all():
        current_norm = card.norm.clothes_list.all()
        employee_clothes_dict = {}
        for clothes in clothes_list:
            if clothes in current_norm:
                list_of_issues = ClothesInCard.objects.filter(card_id=card.id, clothes_id=clothes.id)
                if not list_of_issues:
                    employee_clothes_dict[clothes.id] = 1
                else:
                    last_date = list_of_issues.order_by('-date_of_issue').first().date_of_issue
                    date_ending = last_date + relativedelta(months=clothes.wear_time)
                    if date_ending > date(2022, 12, 31):
                        employee_clothes_dict[clothes.id] = ""
                    else:
                        employee_clothes_dict[clothes.id] = 1
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
