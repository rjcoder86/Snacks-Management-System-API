# Generated by Django 4.0.4 on 2022-05-12 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_meal_meal_count_meal_meal_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='meal_date',
            field=models.DateField(default=''),
        ),
    ]
