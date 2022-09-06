from django.contrib import admin
from app.models import Meal,Order

@admin.register(Meal)
class mealadmin(admin.ModelAdmin):
    list_display = ['id','meal_name','meal_date','meal_penaltyCount']
    ordering = ('-meal_date',)

@admin.register(Order)
class orderadmin(admin.ModelAdmin):
    list_display = ['id','order_date','is_taken']
    ordering = ('-order_date',)
