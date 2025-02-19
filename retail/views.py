from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from retail.models import Company
from retail.serializers import CompanySerializer


class CompanyViewSet(ModelViewSet):

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country']

    def perform_update(self, serializer):

        new_debt = serializer.validated_data.get("debt")

        if new_debt or new_debt == 0:
            raise ValidationError("'Debt' is not allowed to change")

        new_item = serializer.save()
        new_item.save()
