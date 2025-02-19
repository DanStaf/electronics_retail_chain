from django.db import models


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

    debt = models.FloatField(null=True, blank=True, verbose_name='Задолженность перед поставщиком')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    def __str__(self):
        return f'Company: {self.title}'

    class Meta:
        verbose_name = 'компания'
        verbose_name_plural = 'компании'
