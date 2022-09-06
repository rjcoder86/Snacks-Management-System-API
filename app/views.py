import datetime
from django.core.serializers import serialize
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import F
from django.shortcuts import render,get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from django.core import serializers
from .serializer import *
from .models import *
from rest_framework.decorators import api_view, permission_classes

@permission_classes(permissions.IsAdminUser,)
@api_view(['POST'])
def addmeal(request):
     m=Meal.objects.filter(meal_date=request.data['meal_date']).first()
     if m:
         md = MealSerializer(m,data=request.data)
         md.is_valid(raise_exception=True)
         md.save()
     else:
         md = MealSerializer(data=request.data)
         md.is_valid(raise_exception=True)
         md.save()
     return Response({'data':md.data,'msg':'meal added','status':'Success'})

@permission_classes(permissions.IsAdminUser,)
@api_view(['GET'])
def add_guests(request):
    m=Order.objects.filter(is_guest=True,order_date=datetime.datetime.now().date())
    count=int(len(m))
    count2=int(request.GET['count'])
    if count<=count2:
        for i in range(count2-count):
            a = Order.objects.create()
            a.meal_id.set([Meal.objects.filter(meal_date=datetime.datetime.today()).first()])
            a.user_id.set([User.objects.get(is_admin=True)])
            a.is_guest = True
            a.save()
    else:
        for i in range(count-count2):
            m = Order.objects.filter(is_guest=True, order_date=datetime.datetime.now().date()).first()
            m.delete()
    return Response({'msg':f"{request.GET ['count'] } guests added"})

@permission_classes(permissions.IsAuthenticated,)
@api_view(['GET'])
def bookorder(request):
    if datetime.datetime.now().time().hour<21:
        order = Order.objects.filter(user_id=request.user.id, order_date=datetime.datetime.today()).first()
        if not order:
            obj = Order.objects.create()
            obj.user_id.set([User.objects.get(id=request.user.id)])
            obj.meal_id.set((Meal.objects.filter(meal_date=datetime.datetime.today()).first(),))
            obj.save()
            os = OrderSerializer(obj)
            return Response({'data': os.data, 'msg': 'order is placed'})
        return Response({'msg':'You have already ordered your meal'})
    return Response({'msg':'You cannot book meal now'})

@permission_classes(permissions.IsAuthenticated,)
@api_view(['GET'])
def getmyorderdetails(request):
    order = Order.objects.filter(user_id=request.user.id, order_date=datetime.datetime.today()).first()
    if order:
        ms = OrderSerializer(order)
        c=Meal.objects.filter(meal_date__gte=datetime.datetime.now().date()).first()
        d={'meal_name':c.meal_name}
        d.update(ms.data)
        return Response({'data':d,'status':'Success'})
    return Response({'status':'Fail'})


@permission_classes(permissions.IsAdminUser,)
@api_view(['GET'])
def getallorders(request):
    order = Order.objects.all().filter(order_date=datetime.datetime.today())
    os=OrderSerializer(order,many=True)
    return Response(os.data)

@permission_classes(permissions.IsAdminUser,)
@api_view(['GET'])
def geto(request):
    ord = Order.objects.select_related().values('id', 'is_guest', meal_name=F('meal_id__meal_name'),first_name=F('user_id__first_name'))
    ord2=ord.filter(order_date=datetime.datetime.today())
    print(ord2)
    return Response(ord2)

@permission_classes(permissions.IsAdminUser,)
@api_view(['GET'])
def cancleorder(request):
    if datetime.datetime.now().time().hour<20:
        order = Order.objects.filter(user_id=request.user.id, order_date=datetime.datetime.today()).first()
        if order:
            order.delete()
            return Response({'msg': 'Order Cancled','status':'Success'})
        return Response({"msg":"You haven't ordered your meal"})
    return Response({'msg':'You cannot cancel meal now'})

@permission_classes(permissions.IsAdminUser,)
@api_view(['GET'])
def getallmeals(request):
    m=Meal.objects.filter(meal_date__month=datetime.datetime.today().month)
    ms=MealSerializer(m,many=True)
    return Response(ms.data)

@permission_classes(permissions.IsAdminUser,)
@api_view(['GET'])
def getallmealsbydate(request):
    sd = request.GET['startDate']
    ed = request.GET['endDate']
    meals=Meal.objects.all().filter(meal_date__gte=sd,meal_date__lte=ed).values()
    return Response(meals)

@permission_classes(permissions.IsAdminUser,)
@api_view(['GET'])
def guestcount(request):
    m=Order.objects.filter(is_guest=True,order_date=datetime.datetime.now().date())
    return Response({'count':m.count()})

@permission_classes(permissions.IsAuthenticated,)
@api_view(['GET'])
def getmeal(request):
    try:
        m = Meal.objects.filter(meal_date=datetime.datetime.now().date()).first()
    except:
        return Response({'msg':'Meal is not available','status':'Fail'})
    if m:
        orders = Order.objects.all().filter(order_date=datetime.datetime.today())
        m.meal_count = orders.count()
        m.meal_penaltyCount = orders.filter(is_taken=False).count()
        m.save()
        ms = MealSerializer(m)
        return Response(ms.data)
    return Response({'msg':'No meal found'})


@permission_classes(permissions.IsAuthenticated,)
@api_view(['GET'])
def getpo(request):
    sd=request.GET['sd']
    ed=request.GET['ed']
    print(sd,ed)
    meals=Meal.objects.filter(meal_date__gte=sd,meal_date__lte=ed).values('meal_name','meal_date','meal_count','meal_price').order_by('-meal_date')
    # return Response({'msg':'success','data':meals})
    return Response(meals)


@permission_classes(permissions.IsAuthenticated,)
@api_view(['GET'])
def deletemeal(request):
    m=Meal.objects.get(id=int(request.GET['meal_id']))
    Order.objects.filter(order_date=m.meal_date).delete()
    m.delete()
    return Response({'msg':'Meal deleted successfully','status':'Success'})

@permission_classes(permissions.IsAdminUser,)
@api_view(['POST'])
def editmeal(request,id):
    m=Meal.objects.get(id=id)
    ms=MealSerializer(m,data=request.data)
    ms.is_valid(raise_exception=True)
    ms.save()
    return Response(ms.data)

@permission_classes(permissions.IsAuthenticated,)
@api_view(['GET'])
def penalty(request):
    # m=Order.objects.filter(user_id=request.user.id,is_taken=False, order_date__month=datetime.datetime.today().month,order_date__year=datetime.datetime.today().year)
    # ms=OrderSerializer(m,many=True)
    orders = Order.objects.select_related().values('id', 'order_date', 'is_guest', meal_name=F('meal_id__meal_name'),
                                                   first_name=F('user_id__first_name'),
                                                   last_name=F('user_id__last_name'))
    ord = orders.filter(user_id=request.user.id,is_taken=False, is_guest=False,  order_date__month=datetime.datetime.today().month,order_date__year=datetime.datetime.today().year ).order_by('-order_date')

    return Response(ord)

@permission_classes(permissions.IsAuthenticated,)
@api_view(['GET'])
def datepenalty(request):
    sd=request.GET['startDate']
    ed=request.GET['endDate']
    orders = Order.objects.select_related().values('id', 'order_date','is_guest', meal_name=F('meal_id__meal_name'),first_name=F('user_id__first_name'),last_name=F('user_id__last_name'))
    ord=orders.filter(is_taken=False,is_guest=False,order_date__gte=sd,order_date__lte=ed,).order_by('-order_date')
    # ord=orders.filter(order_date__gte=sd,order_date__lte=ed)
    return Response(ord)

@permission_classes(permissions.IsAdminUser,)
@api_view(['GET'])
def singleordertaken(request):
    try:
        id=int(request.GET['order'])
    except ValueError:
        return Response({'status': 'Fail', 'status_code': 604, 'msg': 'Invalid QR Code'})
    try:
        obj=Order.objects.get(id=id)
    except:
        return Response({'status':'Fail','status_code':602,'msg':'Order was canceled'})

    if obj.order_date!= datetime.datetime.now().date() :
        return Response({'status':'Fail','status_code':603,'msg':'Invalid Order for a day'})
    if not obj.is_taken:
        obj.is_taken=True
        obj.save()
        return Response({'status':'Success','status_code':200,'msg':'Order Successfully Delivered'})
    return Response({'status':'Fail','status_code':601,'msg':'meal already taken'})