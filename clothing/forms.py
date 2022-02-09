from django.forms import ModelForm
from .models import Card, Norm, Clothes, Employee
from django import forms

myDateInput = forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {'date_of_birth': myDateInput}


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = '__all__'


class ClothesForm(ModelForm):
    class Meta:
        model = Clothes
        fields = ['clothes_title', 'wear_time', 'nomenclature']


class NormForm(ModelForm):
    class Meta:
        model = Norm
        fields = ['norm_title']