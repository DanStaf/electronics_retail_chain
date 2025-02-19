import rest_framework.serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from retail.models import Company


class CompanySerializer(ModelSerializer):

    level = rest_framework.serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = "__all__"

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

    def validate(self, attrs):

        """
        if no supplier, debt = 0
        if supplier.supplier.supplier - level can't be > 2
        if debt 10.0000005, round

        """

        debt = self._get_actual_value_for_validation(
            attrs,
            "debt"
        )

        supplier = self._get_actual_value_for_validation(
            attrs,
            "supplier"
        )

        if not supplier and not debt == 0:
            raise ValidationError("Please fill 'Supplier' or clear 'Debt'")

        if supplier:
            grand_supplier = supplier.supplier
            if grand_supplier and grand_supplier.supplier:
                raise ValidationError("Company can't use this supplier (allowed only 2 retail levels)")

        attrs["debt"] = round(debt, 2)

        return attrs

    def _get_actual_value_for_validation(self, data_dict, key):
        """
        1) return new value
        2) if not exist return old value
        3) if not exist return None

        :param data_dict:
        :param key:
        :return:
        """

        instance_habit = self.instance

        if key in data_dict:
            # если в словаре есть новое значение
            value = data_dict.get(key)

        elif instance_habit is None:
            # если нет нового значения
            # и нет старого значение
            value = None

        else:
            # если нет нового значения
            # но есть старое значение
            value = getattr(instance_habit, key)  # == instance_habit."key"

        # print(value)

        return value
