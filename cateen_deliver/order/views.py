from itertools import chain

from django.http import HttpResponse
from django.shortcuts import render
from dish.models import Dish, Orders, Assessment
from django.utils import timezone


# Create your views here.

def order(request):
    if not request.session.get('is_login', None):
        print("[DEBUG] 尚未登录")
        message = '尚未登录,请登录'
        return render(request, "./customer/login.html", locals())
    if request.method == 'POST':
        user_id = request.session.get('user_id', None)
        if user_id is not None:
            dish_id = request.POST.get('dish_id')
            print('[DEBUG]', dish_id)
            dish = Dish.objects.get(dish_id=str(dish_id))
    else:
        print('[DEBUG]error')
    return render(request, 'order/order.html', locals())


def payment(request):
    if not request.session.get('is_login', None):
        print("[DEBUG] 尚未登录")
        message = '尚未登录,请登录'
        return render(request, "customer/login.html", locals())
    if request.method == 'POST':
        user_id = request.session.get('user_id', None)
        # 处理评价提交
        ass_order_id = request.POST.get('ass_order_id', None)
        Order = Orders.objects.filter(order_id=ass_order_id)
        print(Order)
        if ass_order_id is not None and len(Order) != 0:
            context = request.POST.get('context', None)
            score = request.POST.get('score', None)
            ass = Assessment.objects.create(
                assessment_id=str(len(Assessment.objects.all()) + 1), order=Orders.objects.get(order_id=ass_order_id), score=int(score), assessment_time=timezone.now(), context=context)
            ass.save()
            message = '评价成功'

        elif ass_order_id is not None:
            message = '订单不存在'
        # 处理订单部分
        else:
            dish_id = request.POST.get('dish_id', None)
            if dish_id is not None:
                dish = Dish.objects.get(dish_id=dish_id)
                dish_num = request.POST.get('dish_num')
                address = request.POST.get('address')
                telephone = request.POST.get('telephone')
                order_id = str(len(Orders.objects.all()) + 1)
                Order = Orders.objects.create(order_id=order_id, dish_num=dish_num, order_status=0, address=address,
                                              telephone=telephone, order_time=timezone.now(), dish_id=dish_id,
                                              user_id=user_id)
                Order.save()
    elif request.method == 'GET':
        user_id = request.session.get('user_id', None)
        Order = Orders.objects.filter(user_id=user_id)
        if Order is None:
            message = '您当前没有订单'
    order_list = Orders.objects.filter(user_id=user_id)
    return render(request, 'order/payment.html', locals())


def ass(request):
    dish_id = request.POST.get('ass_dish_id', None)
    ass_list = []
    if dish_id is None:
        message = '尚无订单'
    else:
        order_list = Orders.objects.filter(dish_id=dish_id)
        for o in order_list:
            ass_list = list(chain(Assessment.objects.filter(order_id=o.order_id), ass_list))
    return render(request, 'order/assessment.html', locals())