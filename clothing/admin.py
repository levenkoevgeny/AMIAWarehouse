from django.contrib import admin
# from .models import Employee, Position, Rank, Subdivision, Card, Norm, Clothes, ClothesInCard, NormItemsInNorm, Group, Course, NormItem, ClothesAggregateInCard, ClothesWithCount

from .models import Employee, Subdivision, Card, Group, Course, Clothes, Position, Rank, NormItem, Norm, NormItemsInNorm, Movement, DescriptionItem


admin.site.register(Employee)
admin.site.register(Subdivision)
admin.site.register(Position)
admin.site.register(Rank)
admin.site.register(Card)
admin.site.register(Norm)
admin.site.register(Clothes)
# admin.site.register(ClothesInCard)
admin.site.register(NormItemsInNorm)
admin.site.register(Group)
admin.site.register(Course)
admin.site.register(NormItem)
admin.site.register(Movement)
admin.site.register(DescriptionItem)

