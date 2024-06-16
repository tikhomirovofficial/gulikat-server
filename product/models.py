from django.db import models
import uuid


def products_image_directory_path(instance: "Products", filename: str) -> str:
    return "products/image_{pk}.jpg".format(
        pk=uuid.uuid4(),
    )


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    
    def __str__(self) -> str:
        return f'{self.title}'
    
    class Meta:
        verbose_name_plural = 'Категории'


class Dimensions(models.Model):
    title = models.CharField(max_length=10, verbose_name="Название")

    def __str__(self) -> str:
        return f'{self.title}'
    
    class Meta:
        verbose_name_plural = 'Единицы измерения'


class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Полное описание")
    price = models.FloatField(verbose_name="Цена")
    discount = models.IntegerField(default=0, verbose_name="Скидка в %")
    weight = models.IntegerField(default=0, verbose_name="Вес")
    dimensions = models.ForeignKey(Dimensions, on_delete=models.CASCADE, default=1, verbose_name="Единица измерения")
    calories = models.IntegerField(default=0, verbose_name="Калории")
    proteins = models.IntegerField(default=0, verbose_name="Белки")
    fats = models.IntegerField(default=0, verbose_name="Жири")
    carbohydrates = models.IntegerField(default=0, verbose_name="углеводы")
    storeg_temperature = models.CharField(max_length=100,default=0, verbose_name="Температура хранения")
    sheif_life = models.CharField(max_length=100,default=0, verbose_name="Время хранения")
    image = models.ImageField(upload_to=products_image_directory_path, default="null.png", verbose_name="Изображение")
    is_activ = models.BooleanField(default=True, verbose_name="Активно?")
    
    def __str__(self) -> str:
        return f'{self.title}'
    
    class Meta:
        verbose_name_plural = 'Товары'

