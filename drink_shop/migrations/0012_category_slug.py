# Generated by Django 3.2.4 on 2021-07-23 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drink_shop', '0011_alter_orderproduct_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
