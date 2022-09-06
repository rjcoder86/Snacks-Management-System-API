from django.urls import path
from . import views


#Admin's URL
urlpatterns = [
    path('addMeal',views.addmeal, name='addMeal'),
    path('addGuestOrder',views.add_guests, name='add_guest'),  #adding guests by count
    path('guestsCount',views.guestcount, name='add_guest'), #giving guest count of today
    path('getAllMeals',views.getallmeals, name='getAllMeals'), #meals of current month
    path('getAllMealsByDate',views.getallmealsbydate, name='getAllMeals'), #meals in given date range
    path('getMeal',views.getmeal, name='register'),  #returns todays meal
    path('getPO',views.getpo, name='register'),   #returns meals for given date range
    path('deleteMeal',views.deletemeal, name='register'), #delete meal of given id
    path('editMeal/<int:id>',views.editmeal, name='editmeal'), #edits meal   ???????
    path('userPenaltyByDate',views.datepenalty, name='penalty'),
    path('getAllOrders',views.getallorders, name='orders'),
    path('getallo',views.geto, name='orders'),
    path('singleOrderTaken',views.singleordertaken, name='ordertaken'),
]

#User's URL
urlpatterns+=[
    path('bookMyOrder', views.bookorder, name='bookmyorder'),
    path('getMyOrderDetails', views.getmyorderdetails, name='getmyorderdetails'),
    path('cancelMyOrder', views.cancleorder, name='cancleorder'),
    path('userPenalty', views.penalty, name='penalty'),

]