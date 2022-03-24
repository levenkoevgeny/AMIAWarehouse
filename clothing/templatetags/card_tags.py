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
    return value.filter(clothes=clothes, movement=1, has_certificate=True).order_by('-date_of_issue').first()


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
        clothes_movement_list = Movement.objects.filter(movement_description=clothes, movement_direction=1,
                                                        has_replacement=False)
        # если выдачи этого наименования не было то выдача в текущем году в количестве по норме
        if clothes_movement_list.count() == 0:
            result_date = datetime.datetime.now().year
            result_count = norm_value_norm_count
        else:
            if norm_value.norm_item.item_clothes.all().count() == 1:
                last_issue = clothes_movement_list.order_by('-date_of_issue').first()
                result_date = last_issue.date_of_issue + relativedelta(months=norm_value_wear_time)
                if result_date.year < datetime.datetime.now().year:
                    result_date = datetime.datetime.now().year
                result_count = norm_value_norm_count
            else:
                last_issue = clothes_movement_list.order_by('-date_of_issue').first()


                # !!!!!!!тут дописать кусок для расчета


                

    else:
        pass

    return '{0} {1} шт.'.format(str(result_date), str(result_count))
