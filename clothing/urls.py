from django.urls import path
from . import views

app_name = 'clothing'

urlpatterns = [
    path('cards', views.card_list, name='card_list'),
    path('card/<card_id>', views.get_card, name='get_card'),
#     path('card-full/<card_id>', views.get_card_full, name='get_card_full'),

    path('clothes', views.clothes_list, name='clothes_list'),
#     path('clothes/sheet', views.get_sheet, name='clothes_sheet'),
    path('norm-items', views.norm_items_list, name='norm_items_list'),

    path('employees', views.employee_list, name='employee_list'),

    path('norms', views.norm_list, name='norm_list'),
    path('norms/<norm_id>/items', views.norm_items, name='norm_items'),
#     # rest-api for making clones based on parent norm
    path('norms/make-clone/', views.make_cloned_norm, name='norm_make_clone'),
    path('movement_several_add', views.movement_several_add, name='movement_several_add'),

    path('random', views.get_random_data, name='random'),
    path('init-dimensions', views.init_dimensions, name='init-dimensions'),
]
