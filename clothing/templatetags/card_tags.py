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
def get_next_date_and_count(movement_list, args):
    result_date = ""
    result_count = ""
    arg_list = [arg.strip() for arg in args.split(',')]
    # получаем арматурную карту
    card = get_object_or_404(Card, pk=arg_list[0])
    # получаем текущее наименование из списка в карте
    clothes = get_object_or_404(Clothes, pk=arg_list[1])

    # получаем норму в арматурной карте
    norm = card.norm

    # получаем список всех наименований в норме
    clothes_in_norm = Clothes.objects.filter(normitem__norm=norm)

    # проверяем в списке ли вещь
    if clothes in clothes_in_norm:
        # первый день текущего полугодия
        current_half_year_start_date = get_current_half_year_start_date()
        norm_value = NormItemsInNorm.objects.filter(norm=norm, norm_item__item_clothes=arg_list[1]).first()
        norm_value_wear_time = norm_value.wear_time
        norm_value_norm_count = norm_value.norm_count
        # print(clothes, norm_value_wear_time, norm_value_norm_count)
        norm_value_wear_time_per_item = norm_value_wear_time / norm_value_norm_count
        # print('norm_value_wear_time_per_item', norm_value_wear_time_per_item)
        clothes_movement_list = movement_list.filter(card=card, movement_description=clothes, movement_direction=1,
                                                     has_replacement=False)

        # если выдачи не было, то выдаем все в этом полугодии
        if clothes_movement_list.count() == 0:
            result_date = current_half_year_start_date
            result_count = norm_value_norm_count
        # если выдачи были
        else:
            # получаем последнюю базовую выдачу
            last_base_issue = clothes_movement_list.filter(is_closed_loop=True).order_by('-date_of_issue').first()
            if last_base_issue:
                term_extension_sum = get_sum_term_extension(last_base_issue)
                start_calculating_date = get_start_calculating_date(last_base_issue,
                                                                    get_remaining_time_from_certificate(last_base_issue))

                # если начальная дата отсчета + срок носки по норме + поправка меньша даты начала текущего полугодия, то
                if start_calculating_date + relativedelta(
                        months=norm_value_wear_time + term_extension_sum) < current_half_year_start_date:
                    result_date = current_half_year_start_date
                    result_count = norm_value_norm_count
                else:
                    # получаем все выдачи от последней базовой до самой последней
                    clothes_movement_list_rest = clothes_movement_list.filter(
                        date_of_issue__gte=last_base_issue.date_of_issue)
                    # просчитываем сумму всех выданных вещей
                    issued_count = 0
                    for item in clothes_movement_list_rest:
                        for desc in item.descriptionitem_set.all():
                            issued_count += desc.count

                    issued_count_normalized = norm_value_norm_count if (
                            issued_count > norm_value_norm_count) else issued_count
                    result_date = start_calculating_date + relativedelta(
                        months=wear_time_normalize(
                            norm_value_wear_time_per_item * issued_count_normalized) + term_extension_sum)
                    if result_date < start_calculating_date:
                        result_date = start_calculating_date
                        result_count = norm_value_norm_count
                    else:
                        needed_count = norm_value_norm_count - issued_count_normalized
                        result_count = norm_value_norm_count if (needed_count == 0) else needed_count

            else:
                pass

        # else:
        #     # получаем последнюю выдачу
        #     last_issue = clothes_movement_list.order_by('-date_of_issue').first()
        #     # print('last_issue', last_issue)
        #     # рассчитываем полную поправку на увеличение срока (когда была замена позиции из аттестата, декрет и т.д.)
        #     term_extension_sum = get_sum_term_extension(last_issue)
        #     # print('term_extension_sum', term_extension_sum)
        #     # рассчитываем дату от которой считаем начало выдачи
        #     # (передаем последнюю выдачу и посчитанный оставшийся срок от сертификата)
        #     start_calculating_date = get_start_calculating_date(last_issue,
        #                                                         get_remaining_time_from_certificate(last_issue))
        #     # print('start_calculating_date', start_calculating_date)
        #     issued_count = 0
        #     for desc in last_issue.descriptionitem_set.all():
        #         issued_count += desc.count
        #
        #     # print('issued_count', issued_count)
        #     # print('months', wear_time_normalize(norm_value_wear_time_per_item * issued_count) + term_extension_sum)
        #     result_date = start_calculating_date + relativedelta(
        #         months=wear_time_normalize(norm_value_wear_time_per_item * issued_count) + term_extension_sum)
        #     # print('result_date', result_date)
        #
        #     if result_date < current_half_year_start_date:
        #         result_date = current_half_year_start_date
        #         result_count = norm_value_norm_count
        #     else:
        #         if last_issue.is_closed_loop:
        #             result_count = norm_value_norm_count if (norm_value_norm_count - issued_count) <= 0 else (
        #                     norm_value_norm_count - issued_count)
        #         else:
        #             last_closing_issue = clothes_movement_list.filter(is_closed_loop=True).order_by(
        #                 '-date_of_issue').first()
        #             if last_closing_issue:
        #                 # оставляем выдачи после последней
        #                 clothes_movement_list_without_last_closing_issue = clothes_movement_list.filter(
        #                     date_of_issue__gt=last_closing_issue.date_of_issue)
        #             else:
        #                 clothes_movement_list_without_last_closing_issue = clothes_movement_list
        #
        #             issued_count = 0
        #             for item in clothes_movement_list_without_last_closing_issue:
        #                 for desc in item.descriptionitem_set.all():
        #                     issued_count += desc.count
        #             result_count = norm_value_norm_count if (norm_value_norm_count - issued_count) <= 0 else (
        #                     norm_value_norm_count - issued_count)

    month = result_date.strftime("%m") if result_date else ""
    separator = "." if result_date else ""
    year = result_date.strftime("%y") if result_date else ""
    unit = "шт." if result_date else ""

    return '{0}{1}{2} {3} {4}'.format(month, separator, year, str(result_count), unit)


def wear_time_normalize(wear_time):
    if 6 < wear_time <= 12:
        return 12
    if 12 < wear_time < 24:
        return 12
    return wear_time


def next_date_of_issue_normalize(next_date_of_issue):
    current_half_year_start_date = get_current_half_year_start_date()
    if next_date_of_issue < current_half_year_start_date:
        return current_half_year_start_date
    return next_date_of_issue


def count_normalize(norm_count, issued_count):
    pass


def get_current_half_year_start_date():
    current_date = datetime.datetime.now()
    if 1 < current_date.month <= 6:
        return datetime.date(current_date.year, 1, 1)
    if 6 < current_date.month <= 12:
        return datetime.date(current_date.year, 7, 1)


def get_current_half_year_end_date():
    current_date = datetime.datetime.now()
    if 1 < current_date.month <= 6:
        return datetime.date(current_date.year, 6, 30)
    if 6 < current_date.month <= 12:
        return datetime.date(current_date.year, 12, 31)


def get_remaining_time(issue):
    # считаем сколько времени эта вещь носилась
    elapsed_time = relativedelta(issue.date_of_issue, issue.replacing_what.date_of_issue)

    years = elapsed_time.years if elapsed_time.years else 0
    months = elapsed_time.months if elapsed_time.months else 0

    # переводим это число в количество месяцев
    elapsed_time_month = years * 12 + months

    # проверяем не закончился ли срок носки вещи из аттестата
    remaining_term = 0 if (issue.replacing_what.certificate_wear_time - elapsed_time_month) <= 0 else elapsed_time_month
    return remaining_term


def get_remaining_time_from_certificate(issue):
    if issue.replacing_what:
        # считаем сколько времени эта вещь носилась
        elapsed_time = relativedelta(issue.date_of_issue, issue.replacing_what.date_of_issue)

        years = elapsed_time.years if elapsed_time.years else 0
        months = elapsed_time.months if elapsed_time.months else 0

        # переводим это число в количество месяцев
        elapsed_time_month = years * 12 + months

        # проверяем не закончился ли срок носки вещи из аттестата
        remaining_term = 0 if (
                                      issue.replacing_what.certificate_wear_time - elapsed_time_month) <= 0 else elapsed_time_month
        return remaining_term
    else:
        return 0


def get_start_calculating_date(issue, term_extension):
    if issue.replacing_what:
        return issue.date_of_issue if term_extension == 0 else issue.replacing_what.date_of_issue
    else:
        return issue.date_of_issue


def get_sum_term_extension(issue):
    remaining = 0
    if issue.replacing_what:
        remaining += get_remaining_time_from_certificate(issue)
    return remaining
