# Generated by Django 4.0.4 on 2022-05-27 12:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_meal_meal_penaltycount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.date(2022, 5, 27)),
        ),
    ]
