# Generated by Django 3.2.4 on 2021-07-25 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drink_shop', '0013_auto_20210725_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='abv',
            field=models.FloatField(blank=True, null=True, verbose_name='ABV'),
        ),
    ]