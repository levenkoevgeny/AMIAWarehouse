from django.urls import path
from . import views

app_name = 'clothing'

urlpatterns = [
    path('cards', views.card_list, name='card_list'),
    path('card/input', views.card_input, name='card_input'),
    path('card/<card_id>', views.get_card, name='get_card'),
    path('card-full/<card_id>', views.get_card_full, name='get_card_full'),
    path('card/<card_id>/update', views.card_update, name='card_update'),

    path('clothes', views.clothes_list, name='clothes_list'),
    path('clothes/input', views.clothes_input, name='clothes_input'),
    path('clothes/<clothes_id>/update', views.clothes_update, name='clothes_update'),
    path('clothes/sheet', views.get_sheet, name='clothes_sheet'),

    path('employees', views.employee_list, name='employee_list'),
    path('employees/input', views.employee_input, name='employee_input'),
    path('employees/<employee_id>/<card_id>/update', views.employee_update, name='employee_update'),

]