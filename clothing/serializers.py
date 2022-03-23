from rest_framework import serializers
from .models import Clothes, NormItem, Norm, NormItemsInNorm, Employee, Card, Movement, DescriptionItem


class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = '__all__'


class NormItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormItem
        fields = '__all__'


class NormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Norm
        fields = '__all__'


class NormItemsInNormSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormItemsInNorm
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = '__all__'


class DescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptionItem
        fields = '__all__'