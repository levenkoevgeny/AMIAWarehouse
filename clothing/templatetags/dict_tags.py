from django import template

register = template.Library()


@register.filter(name='get_sub_dict')
def get_sub_dict(value, index):
    return value[index]




    # arg_list = [arg.strip() for arg in args.split(',')]
    # return value.subject_set.filter(level__level_title=arg_list[0]).filter(guids__kind__kind_name=arg_list[1],
    #                                                                        guids__grif__grif_name=arg_list[2]).count()
