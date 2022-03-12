from django import template
register = template.Library()


@register.filter(name='mult')
def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)


@register.filter(name='str_concat')
def str_concat(value, arg):
    "Concat the arg and the value"
    return str(value) + ', ' + str(arg)