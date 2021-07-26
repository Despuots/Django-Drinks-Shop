# Generated by Django 3.2.4 on 2021-07-16 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drink_shop', '0005_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cover',
            field=models.ImageField(null=True, upload_to='category_covers', verbose_name='Cover'),
        ),
        migrations.AddField(
            model_name='product',
            name='cover',
            field=models.ImageField(null=True, upload_to='product_covers', verbose_name='Cover'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Price'),
        ),
    ]