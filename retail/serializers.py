import rest_framework.serializers
from rest_framework.serializers import ModelSerializer

from retail.models import Company


class CompanySerializer(ModelSerializer):

    level = rest_framework.serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = "__all__"
        #exclude = ['debt']

    def get_level(self, obj):
        parent_supplier = obj.supplier
        if not parent_supplier:
            return 0
        else:
            grand_supplier = parent_supplier.supplier
            if not grand_supplier:
                return 1
            else:
                return 2
