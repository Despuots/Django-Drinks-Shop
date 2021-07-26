# Generated by Django 3.2.4 on 2021-07-25 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drink_shop', '0012_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='abv',
            field=models.IntegerField(blank=True, null=True, verbose_name='ABV'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_region',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Product region'),
        ),
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='Featured'),
        ),
    ]