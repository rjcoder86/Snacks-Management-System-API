# Generated by Django 4.0.4 on 2022-05-11 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_mealclass_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_guest',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Mealclass',
        ),
    ]
