from django.forms import ModelForm
from .models import Card, Norm, Clothes
from django import forms


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = '__all__'


class ClothesForm(ModelForm):
    class Meta:
        model = Clothes
        fields = ['clothes_title', 'wear_time', 'nomenclature']