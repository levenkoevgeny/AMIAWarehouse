from django.contrib import admin
from .models import Employee, Position, Rank, Subdivision, Card, Norm, Clothes, ClothesInCard, ClothesInNorm, Group, Course

admin.site.register(Employee)
admin.site.register(Subdivision)
admin.site.register(Position)
admin.site.register(Rank)
admin.site.register(Card)
admin.site.register(Norm)
admin.site.register(Clothes)
admin.site.register(ClothesInCard)
admin.site.register(ClothesInNorm)
admin.site.register(Group)
admin.site.register(Course)
