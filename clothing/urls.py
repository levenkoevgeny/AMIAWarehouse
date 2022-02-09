from django.urls import path
from . import views

app_name = 'clothing'

urlpatterns = [
    path('cards', views.card_list, name='card_list'),
    path('card/input', views.card_input, name='card_input'),
    path('card/<card_id>', views.get_card, name='get_card'),
    path('card/<card_id>/update', views.get_card, name='card_update'),

    # path('clothes', views.card_update, name='clothes_list'),
    # path('clothes/input', views.card_update, name='clothes_update'),
    # path('clothes/<clothes_id>/update', views.card_update, name='clothes_update'),
    path('clothes/sheet', views.get_sheet, name='clothes_sheet'),

]