from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from retail.models import Company
from retail.serializers import CompanySerializer


class CompanyViewSet(ModelViewSet):

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
