# Generated by Django 4.0.4 on 2022-05-11 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0002_remove_order_meal_id_remove_order_user_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_name', models.CharField(max_length=40)),
                ('meal_date', models.DateField(auto_now_add=True)),
                ('meal_description', models.TextField(max_length=100)),
            ],
        ),
    ]
