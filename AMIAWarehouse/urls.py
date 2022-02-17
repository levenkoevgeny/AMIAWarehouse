"""AMIAWarehouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from rest_framework import routers
from clothing import views


router = routers.DefaultRouter()
router.register(r'clothes-in-card', views.ClothesInCardViewSet)
router.register(r'cards', views.CardViewSet)
router.register(r'norms', views.NormViewSet)
router.register(r'norms-items', views.ClothesInNormViewSet)
router.register(r'clothes', views.ClothesViewSet)
router.register(r'employees', views.EmployeeViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url="/clothing/cards")),
    path('clothing/', include('clothing.urls')),
    path('api/', include(router.urls)),
]
