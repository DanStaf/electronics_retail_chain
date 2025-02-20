from django.db import models
from rest_framework.exceptions import ValidationError


class Product(models.Model):
    """
    название,
    модель,
    дата выхода продукта на рынок.
    """

    title = models.CharField(max_length=150, verbose_name='Название')
    model = models.CharField(null=True, blank=True,
                             max_length=150, verbose_name='Модель')
    release_date = models.DateField(null=True, blank=True,
                                    verbose_name='Дата выхода продукта на рынок')

    def __str__(self):
        return f'Product: {self.title}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Company(models.Model):
    """
    Название.
    Тип компании.
    Контакты:
        email,
        страна,
        город,
        улица,
        номер дома.
    Продукты.
    Поставщик (предыдущий по иерархии объект сети).
    Задолженность перед поставщиком в денежном выражении с точностью до копеек.
    Время создания (заполняется автоматически при создании).
    """

    COMPANY_CHOICES = [
        ("Завод", "Завод"),
        ("Розничная сеть", "Розничная сеть"),
        ("Индивидуальный предприниматель", "Индивидуальный предприниматель")
    ]

    title = models.CharField(max_length=150, verbose_name='Название')

    type = models.CharField(max_length=150, choices=COMPANY_CHOICES, verbose_name='Тип компании')

    email = models.EmailField(null=True, blank=True, verbose_name='E-mail')
    country = models.CharField(null=True, blank=True, max_length=50, verbose_name='Страна')
    city = models.CharField(null=True, blank=True, max_length=50, verbose_name='Город')
    street = models.CharField(null=True, blank=True, max_length=50, verbose_name='Улица')
    building = models.CharField(null=True, blank=True, max_length=50, verbose_name='Номер дома')

    products = models.ManyToManyField("retail.Product", verbose_name='Продукты')

    supplier = models.ForeignKey("retail.Company",
                                 null=True, blank=True,
                                 verbose_name='Поставщик',
                                 on_delete=models.SET_NULL)

    debt = models.FloatField(default=0.0,
                             verbose_name='Задолженность перед поставщиком')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    def __str__(self):
        return f'Company: {self.title}'

    def clean(self, *args, **kwargs):
        # add custom validation here

        if not self.supplier and not self.debt == 0:
            raise ValidationError("Please fill 'Supplier' or clear 'Debt'")

        if self.supplier and self.supplier == self:
            raise ValidationError("'Supplier' can't be the Company itself")

        if self.supplier:

            # print(f"есть родитель: {self.supplier}")

            grand_supplier = self.supplier.supplier
            if grand_supplier:
                # print(f"есть дед: {grand_supplier}")

                if grand_supplier.supplier:
                    raise ValidationError("Company can't use this supplier (allowed only 2 retail levels)")
                # else:
                #     print("ОК. нет прадеда")

                children = self._get_children()

                if children:
                    raise ValidationError("Company can't use this supplier (allowed only 2 retail levels)")
                # else:
                #     print("ОК. нет детей")
            else:

                # print("нет деда")
                children = self._get_children()

                if children:
                    second_children = self._get_children(children)
                else:
                    second_children = None

                # print(children)
                # print(second_children)

                # children.children - если не пусто - ошибка
                if second_children:
                    raise ValidationError("Company can't use this supplier (allowed only 2 retail levels)")
                # else:
                #     print("ОК. нет внуков")
        else:
            # print("нет родителя")

            children = self._get_children()

            if children:
                second_children = self._get_children(children)
            else:
                second_children = None

            if second_children:
                third_children = self._get_children(second_children)
            else:
                third_children = None

            # print(children)
            # print(second_children)
            # print(third_children)
            # children.children.children - если не пусто - ошибка

            if third_children:
                raise ValidationError("Company can't use this supplier (allowed only 2 retail levels)")
            # else:
            #     print("ОК. нет правнуков")

        self.debt = round(self.debt, 2)

        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def _get_children(self, instance_set=None):

        if instance_set:
            return Company.objects.filter(supplier__in=instance_set).exclude(pk=self.pk)
        else:
            return Company.objects.filter(supplier=self).exclude(pk=self.pk)

    class Meta:
        verbose_name = 'компания'
        verbose_name_plural = 'компании'
