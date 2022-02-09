from rest_framework import serializers
from .models import ClothesInCard, Card, Norm, Clothes


class ClothesInCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesInCard
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class NormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Norm
        fields = '__all__'


class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = '__all__'

