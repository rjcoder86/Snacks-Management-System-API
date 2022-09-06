from datetime import datetime

from rest_framework import serializers

from account.models import User
from app.models import Meal, Order

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model=Meal
        fields='__all__'

class mealser(serializers.ModelSerializer):
    class Meta:
        model=Meal
        fields=['meal_name']

class userser(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name']

class OrderSerializer(serializers.ModelSerializer):
    meal_id=mealser(many=True)
    user_id=userser(many=True)
    class Meta:
        model=Order
        fields='__all__'

class orderser2(serializers.Serializer):
    meal_id = MealSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


