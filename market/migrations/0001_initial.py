# Generated by Django 5.0 on 2024-01-06 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Адрес')),
                ('long', models.FloatField(default=0.0, verbose_name='Долгота')),
                ('lat', models.FloatField(default=0.0, verbose_name='Широта')),
                ('is_main_for_siti', models.BooleanField(default=False, verbose_name='Основной для города?')),
                ('is_activ', models.BooleanField(default=True, verbose_name='Активен?')),
            ],
            options={
                'verbose_name_plural': 'Адреса магазинов',
            },
        ),
        migrations.CreateModel(
            name='Siti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название города')),
            ],
            options={
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='ProductsInAdress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, verbose_name='Количество')),
                ('adress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.adress', verbose_name='Адрес')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.products', verbose_name='Продукт')),
            ],
        ),
        migrations.AddField(
            model_name='adress',
            name='siti',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.siti', verbose_name='Город'),
        ),
    ]
