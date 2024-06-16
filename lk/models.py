from django.db import models
from django.contrib.auth.models import User


class Adress(models.Model):
    adress = models.CharField(max_length=500, verbose_name="Адрес")
    entrance = models.IntegerField(blank=True, default="0", verbose_name="Подъезд")
    floor = models.IntegerField(blank=True, default="0", verbose_name="Этаж")
    door_code = models.IntegerField(blank=True, default="0", verbose_name="Код двери")
    apartment = models.IntegerField(blank=True, default="0", verbose_name="Квартира")
    long = models.FloatField(default=0.0, verbose_name="Долгота")
    lat = models.FloatField(default=0.0, verbose_name="Широта")
    is_activ = models.BooleanField(default=True, verbose_name="Активен?")
    
    def __str__(self) -> str:
        return f'{self.adress}'
    
    class Meta:
        verbose_name_plural = 'Адреса'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    dob = models.CharField(max_length=10, default="", blank=True, verbose_name="Дата рождения")
    adress = models.ManyToManyField(Adress, blank=True, verbose_name="Адреса")
    
    def __str__(self) -> str:
        return f'{self.user}'
    
    class Meta:
        verbose_name_plural = 'Профили пользователей'

