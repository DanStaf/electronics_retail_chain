from django.urls import path, include
from retail.apps import RetailConfig
from rest_framework import routers

from retail.views import CompanyViewSet

app_name = RetailConfig.name

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')

urlpatterns = [
    path('', include(router.urls)),

]
