# Generated by Django 4.0.4 on 2022-05-17 12:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_meal_meal_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.date(2022, 5, 17)),
        ),
    ]