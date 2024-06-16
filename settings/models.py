from django.db import models


class OrderSettings(models.Model):
    min_prise_auto = models.FloatField(verbose_name="Минимальная сумма заказа для автодоставки")
    auto_free_delivery = models.BooleanField(default=True, verbose_name="Бесплатная доставка?")
    auto_price_delivery = models.FloatField(default=0.0, blank=True, verbose_name="Цена атодоставки")
    min_prise_people = models.FloatField(verbose_name="Минимальная сумма заказа для пешей доставки")
    people_free_delivery = models.BooleanField(default=True, verbose_name="Бесплатная доставка")
    people_price_delivery = models.FloatField(default=0.0, blank=True, verbose_name="Цена пешей доставки")
    people_long_delivery = models.IntegerField(default=1500, verbose_name="Дальность пешей доставки")

    def __str__(self) -> str:
        return f'Стоимость доставки'
    
    class Meta:
        verbose_name_plural = 'Настройки заказов'


class ErrorClient(models.Model):
    datetime = models.CharField(max_length=500)
    sent_data = models.JSONField()
    received_response = models.TextField()
    status = models.CharField(max_length=100)
    user = models.CharField(max_length=500)
    url = models.CharField(max_length=500)

    def __str__(self) -> str:
        return f'{self.datetime}'
    
    class Meta:
        verbose_name_plural = 'Ошибки'


class AllProductsSettings(models.Model):
    total_discount = models.IntegerField(verbose_name="Общая скидка в %", default=0)

    def __str__(self) -> str:
        return f'Настройки товаров'
    
    class Meta:
        verbose_name_plural = 'Настройки товаров'


class GlobalSettings(models.Model):
    is_dev = models.BooleanField(default=False, verbose_name="Режим разработки")
    is_disabled_cart = models.BooleanField(default=False, verbose_name="Отключить корзину")
    is_disabled_online_pyment = models.BooleanField(default=False, verbose_name="Отключить онлайн оплату")
    is_disabled_cash_pyment = models.BooleanField(default=False, verbose_name="Отключить отплату наличными")
    is_disabled_auto_delivery = models.BooleanField(default=False, verbose_name="Отключить автодоставку")
    is_disabled_people_delivery = models.BooleanField(default=False, verbose_name="Отклюить пешую доставку")
    is_disabled_pickup_delivery = models.BooleanField(default=False, verbose_name="Отключить самовывоз")
    is_disabled_reservation = models.BooleanField(default=False, verbose_name="Отключить бронирование столиков")
    is_disabled_order = models.BooleanField(default=False, verbose_name="Отключить бронирование столиков")

    def __str__(self) -> str:
        return f'Глобальные настройки'
    
    class Meta:
        verbose_name_plural = 'Глобальные настройки'
