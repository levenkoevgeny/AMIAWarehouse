from django.forms import ModelForm
from .models import Card, Employee, Decree, Clothes, NormItem, Norm, NormItemsInNorm
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


class NormItemForm(ModelForm):
    class Meta:
        model = NormItem
        fields = '__all__'


class NormForm(ModelForm):
    class Meta:
        model = Norm
        fields = ['norm_title']


class NormItemsInNormForm(ModelForm):
    class Meta:
        model = NormItemsInNorm
        fields = '__all__'


class DecreeForm(ModelForm):
    class Meta:
        model = Decree
        fields = '__all__'
