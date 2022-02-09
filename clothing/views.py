from django.shortcuts import render

from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.urls import reverse

from .models import Card, Clothes, Norm, ClothesInCard, Employee
from .forms import CardForm, ClothesForm

from django.forms.models import model_to_dict
from datetime import datetime, date
from dateutil.relativedelta import *

from rest_framework import viewsets
from .serializers import ClothesInCardSerializer, CardSerializer, NormSerializer, ClothesSerializer
from .filters import CardFilter


def card_list(request):
    f = CardFilter(request.GET, queryset=Card.objects.all())
    card_list = f.qs

    return render(request, 'clothing/card/card_list.html', {'card_list': card_list, 'filter': f})


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


def get_card(request, card_id):
    if request.method == 'POST':
        pass
    else:
        card = get_object_or_404(Card, pk=card_id)
        form = CardForm(instance=card)
        norm_clothes_list = card.norm.clothes_list.all()

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
                      {'form': form, 'card': card, 'norm_clothes_list': norm_clothes_list, 'result_list': result_list,
                       'year_list': year_list, 'clothes_list': Clothes.objects.all()})


def card_update(request, card_id):
    if request.method == 'POST':
        obj = get_object_or_404(Card, pk=card_id)
        form = CardForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('clothing:card_list'))
    else:
        pass


def card_delete(request):
    pass


def clothes_input(request):
    pass


def clothes_update(request, clothes_id):
    pass


def clothes_delete(request):
    pass


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

    return render(request, 'clothing/sheet.html',
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
