# Generated by Django 3.2.4 on 2021-07-16 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drink_shop', '0004_alter_product_category_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Price'),
        ),
    ]
