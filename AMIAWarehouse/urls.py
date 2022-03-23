from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from rest_framework import routers
from clothing import views


router = routers.DefaultRouter()

router.register(r'clothes', views.ClothesViewSet)
router.register(r'norms-items', views.NormItemViewSet)
router.register(r'norms', views.NormViewSet)
router.register(r'norms-items-in-norm', views.NormItemsInNormViewSet)
router.register(r'cards', views.CardViewSet)
router.register(r'movements', views.MovementViewSet)
router.register(r'description-item', views.DescriptionItemViewSet)
router.register(r'employees', views.EmployeeViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url="/clothing/cards")),
    path('clothing/', include('clothing.urls')),
    path('api/', include(router.urls)),
]
