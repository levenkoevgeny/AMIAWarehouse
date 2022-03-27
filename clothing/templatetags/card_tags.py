from django import template
import datetime
from django.shortcuts import get_object_or_404

from clothing.models import Card, NormItemsInNorm, Clothes, DescriptionItem, Movement

from dateutil.relativedelta import *

register = template.Library()


@register.filter(name='get_movement_out')
def get_movement_out(value, args):
    arg_list = [arg.strip() for arg in args.split(',')]
    return value.filter(date_of_issue__year=arg_list[0], norm_item=arg_list[1], movement_direction=1,
                        has_certificate=False)


@register.filter(name='get_movement_in')
def get_movement_in(value, args):
    arg_list = [arg.strip() for arg in args.split(',')]
    return value.filter(date_of_issue__year=arg_list[0], clothes=arg_list[1], movement_direction=2,
                        has_certificate=False)


@register.filter(name='get_descriptions_out')
def get_descriptions_out(value, args):
    arg_list = [arg.strip() for arg in args.split(',')]
    return value.filter(movement__date_of_issue__year=arg_list[0], clothes=arg_list[1], movement__movement_direction=1,
                        movement__has_certificate=False)


@register.filter(name='get_descriptions_in')
def get_descriptions_out(value, args):
    arg_list = [arg.strip() for arg in args.split(',')]
    return value.filter(movement__date_of_issue__year=arg_list[0], clothes=arg_list[1], movement__movement_direction=2,
                        movement__has_certificate=False)


@register.filter(name='get_certificate_item')
def get_certificate_item(value, clothes):
    return value.filter(clothes=clothes, movement__has_certificate=True).order_by('-id').first()


@register.filter(name='get_next_date_and_count')
def get_next_date_and_count(value, args):
    result_date = ""
    result_count = ""
    arg_list = [arg.strip() for arg in args.split(',')]
    # получаем арматурную карту
    card = get_object_or_404(Card, pk=arg_list[0])
    # получаем норму в арматурной карте
    norm = card.norm

    # получаем текущее наименование из списка в карте
    clothes = get_object_or_404(Clothes, pk=arg_list[1])

    # получаем список всех наименований в норме
    clothes_in_norm = Clothes.objects.filter(normitem__norm=norm)

    # проверяем в списке ли вещь
    if clothes in clothes_in_norm:
        norm_value = NormItemsInNorm.objects.filter(norm=norm, norm_item__item_clothes=arg_list[1]).first()
        norm_value_wear_time = norm_value.wear_time
        norm_value_norm_count = norm_value.norm_count
        clothes_movement_list = Movement.objects.filter(card=card, movement_description=clothes, movement_direction=1,
                                                        has_replacement=False)
        # если выдачи этого наименования не было то выдача в текущем году в количестве по норме
        if clothes_movement_list.count() == 0:
            result_date = datetime.datetime.now().year
            result_count = norm_value_norm_count
        else:
            # если позиция нормы состоит из одной вещи
            if norm_value.norm_item.item_clothes.all().count() == 1:
                last_issue = clothes_movement_list.order_by('-date_of_issue').first()

                # Проверить была ли эта выдача заменой позиции из аттестата
                # если да, то дату выдачи берем из аттестата
                if last_issue.replacing_what:
                    result_date = last_issue.replacing_what.date_of_issue + relativedelta(months=norm_value_wear_time)
                else:
                    result_date = last_issue.date_of_issue + relativedelta(months=norm_value_wear_time)

                if result_date.year < datetime.datetime.now().year:
                    result_date = datetime.datetime.now().year
                result_count = norm_value_norm_count
            # случай, если позиция нормы состоит более чем из одной вещи
            else:
                # получает норму на единицу
                norm_value_wear_time_per_item = norm_value_wear_time / norm_value_norm_count
                # проверяем есть ли замыкающие выдачи
                # если есть то
                if clothes_movement_list.filter(is_closed_loop=True).count() > 0:
                    # получаем последнюю замыкающую выдачу
                    last_closing_loop = clothes_movement_list.filter(is_closed_loop=True).order_by(
                        '-date_of_issue').first()
                    # получаем остальные выдачи (после последней замыкающей)
                    clothes_movement_list_without_closing_loop = clothes_movement_list.filter(
                        date_of_issue__gt=last_closing_loop.date_of_issue)
                    # если спискок пуст (т.е. замыкающая выдача была последней)
                    if clothes_movement_list_without_closing_loop.count() == 0:
                        # вычисляем сколько вещей было выдано в последней замыкающей выдаче, чтобы узнать дату следующей выдачи
                        issued_count = 0
                        for desc in last_closing_loop.descriptionitem_set.all():
                            issued_count += desc.count

                        # проверяем выдана ли вся норма
                        if issued_count < norm_value_norm_count:
                            result_date = next_date_of_issue_normalize(last_closing_loop.date_of_issue + relativedelta(
                                months=wear_time_normalize(norm_value_wear_time_per_item) * issued_count))
                            result_count = norm_value_norm_count
                        # выдана не вся норма
                        else:
                            # вычисляем дату следующей выдачи и нормализуем ее (т.е. проверяем не меньше ли она текущего года)
                            result_date = next_date_of_issue_normalize(last_closing_loop.date_of_issue + relativedelta(
                                months=norm_value_wear_time))
                            result_count = norm_value_norm_count
                    else:
                        # список не пуст (т.е. были выдачи после последней замыкающей)
                        # получаем последнюю выдачу
                        last_issue = clothes_movement_list_without_closing_loop.last()
                        last_issue_next_date = last_issue.date_of_issue + relativedelta(months=wear_time_normalize(norm_value_wear_time_per_item))
                        # если дата следующей выдачи уже прошла
                        if last_issue_next_date.year < datetime.datetime.now().year:
                            result_date = datetime.datetime.now().year
                            result_count = norm_value_norm_count
                        # если дата следующей выдачи еще не прошла
                        else:
                            issued_count = 0
                            for cl in clothes_movement_list_without_closing_loop:
                                for desc in cl.descriptionitem_set.all():
                                    issued_count += desc.count
                            if issued_count < norm_value_norm_count:
                                result_date = last_issue.date_of_issue + relativedelta(
                                    months=wear_time_normalize(norm_value_wear_time_per_item) * issued_count)
                                result_count = norm_value_norm_count - issued_count
                            else:
                                result_date = last_issue.date_of_issue + relativedelta(months=norm_value_wear_time)
                                result_count = norm_value_norm_count
                # если нету то
                else:
                    last_issue = clothes_movement_list.last()
                    last_issue_next_date = last_issue.date_of_issue + relativedelta(
                        months=wear_time_normalize(norm_value_wear_time_per_item))
                    # если дата следующей выдачи уже прошла
                    if last_issue_next_date.year < datetime.datetime.now().year:
                        result_date = datetime.datetime.now().year
                        result_count = norm_value_norm_count
                    # если дата следующей выдачи еще не прошла
                    else:
                        issued_count = 0
                        for cl in clothes_movement_list:
                            for desc in cl.descriptionitem_set.all():
                                issued_count += desc.count
                        if issued_count < norm_value_norm_count:
                            result_date = last_issue.date_of_issue + relativedelta(
                                months=wear_time_normalize(norm_value_wear_time_per_item) * issued_count)
                            result_count = norm_value_norm_count - issued_count
                        else:
                            result_date = last_issue.date_of_issue + relativedelta(months=norm_value_wear_time)
                            result_count = norm_value_norm_count

    else:
        pass

    if result_count:
        unit = "шт."
    else:
        unit = ""

    return '{0} {1} {2}'.format(str(result_date), str(result_count), unit)


def wear_time_normalize(wear_time):
    if 6 < wear_time <= 12:
        return 12
    if 12 < wear_time <= 24:
        return 12


def next_date_of_issue_normalize(next_date_of_issue):
    return next_date_of_issue

def count_normalize(norm_count, issued_count):
    pass
