import datetime

from django.db import models
from account.models import User

class Meal(models.Model):
    meal_name=models.CharField(max_length=40)
    meal_date=models.DateField(unique=True)
    meal_description=models.TextField(max_length=100,default='',blank=True)
    meal_count=models.IntegerField(default=0)
    meal_price=models.FloatField(default=0)
    meal_penaltyCount=models.IntegerField(default=0)
    # def __str__(self):
    #     return self.meal_name

class Order(models.Model):
    order_date=models.DateField(default=datetime.datetime.now().date())
    meal_id=models.ManyToManyField(Meal)
    user_id=models.ManyToManyField(User)
    is_guest=models.BooleanField(default=False)
    is_taken=models.BooleanField(default=False)

