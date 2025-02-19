from django.urls import path, include
from retail.apps import RetailConfig
from rest_framework import routers

app_name = RetailConfig.name

#router_course = routers.DefaultRouter()
#router_course.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
#    path('', include(router_course.urls)),

]
