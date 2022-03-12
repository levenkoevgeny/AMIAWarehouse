from django import template

register = template.Library()


@register.filter(name='get_movement_out')
def get_movement_out(value, args):
    arg_list = [arg.strip() for arg in args.split(',')]
    return value.filter(date_of_issue__year=arg_list[0], clothes=arg_list[1], movement=1, has_certificate=False)


@register.filter(name='get_movement_in')
def get_movement_in(value, args):
    arg_list = [arg.strip() for arg in args.split(',')]
    return value.filter(date_of_issue__year=arg_list[0], clothes=arg_list[1], movement=2, has_certificate=False)


@register.filter(name='get_certificate_item')
def get_certificate_item(value, clothes):
    return value.filter(clothes=clothes, movement=1, has_certificate=True).order_by('-date_of_issue').first()