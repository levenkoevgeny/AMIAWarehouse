from django.forms import ModelForm
from .models import Card, Norm, Clothes, Employee, ClothesInNorm
from django import forms

myDateInput = forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {'date_of_birth': myDateInput,
                   'decree_start': myDateInput,
                   'decree_finish': myDateInput,
                   'enlisted': myDateInput,
                   'excluded': myDateInput,
                   }


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = '__all__'


class ClothesForm(ModelForm):
    class Meta:
        model = Clothes
        fields = '__all__'


class NormForm(ModelForm):
    class Meta:
        model = Norm
        fields = ['norm_title']


class ClothesInNormForm(ModelForm):

    class Meta:
        model = ClothesInNorm
        fields = '__all__'
