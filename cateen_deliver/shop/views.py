from django.shortcuts import render
from django.utils import timezone
from dish.models import Dish, Stall, Userinfo, Orders
from itertools import chain

# Create your views here.


def shop_manage(request):
    if not request.session.get('is_login', None):
        print("[DEBUG] 尚未登录")
        message = '尚未登录,请登录'
        return render(request, "shop/shop_base.html", locals())
    if request.method == 'GET':
        user_id = request.session.get('user_id', None)
        if user_id is not None:
            stalls = Stall.objects.filter(user_id=user_id)
            print(stalls)
            if len(stalls) == 0:
                message = '您不是商家，请返回主页点餐'
                return render(request, 'shop/shop_base.html', locals())
            else:
                stall = stalls[0]
                return render(request, 'shop/shop_base.html', locals())
    return render(request, 'shop/shop_base.html', locals())


def shop_order(request):
    user_id = request.session.get('user_id', None)
    if request.method == 'GET':
        dish = Dish.objects.filter(stall_id=user_id)
        order_list = []
        for d in dish:
            order_list = list(chain(Orders.objects.filter(dish_id=d.dish_id), order_list))
        if order_list is None:
            message = '您当前没有订单'
            return render(request, 'shop/shop_order.html', locals())
        return render(request, 'shop/shop_order.html', locals())
    if request.method == 'POST':
        order_id = request.POST.get('stall_order_id', None)
        print(order_id)
        if order_id is not None:
            order_change = Orders.objects.get(order_id=order_id)
            order_change.order_status = 1
            order_change.save()
        dish = Dish.objects.filter(stall_id=user_id)
        order_list = []
        for d in dish:
            order_list = list(chain(Orders.objects.filter(dish_id=d.dish_id), order_list))
        if order_list is None:
            message = '您当前没有订单'
            return render(request, 'shop/shop_order.html', locals())
    return render(request, 'shop/shop_order.html', locals())


def shop_dish(request):
    user_id = request.session.get('user_id', None)
    if request.method == 'GET':
        dish_list = Dish.objects.filter(stall_id=user_id)
        if dish_list is None:
            message = '您当前没有菜品'
    elif request.method == 'POST':
        dish_id = request.POST.get('stall_dish_id', None)
        # 处理删除部分
        if dish_id is not None:
            Dish.objects.get(dish_id=dish_id).delete()
            dish_list = Dish.objects.filter(stall_id=user_id)
            return render(request, 'shop/shop_dish.html', locals())
        # 创建部分
        dish_name = request.POST.get('dish_name', None)
        dish_price = request.POST.get('dish_price', None)
        dish_description = request.POST.get('dish_description', None)
        search_dict = dict()
        search_dict['stall_id'] = user_id
        search_dict['dish_name'] = dish_name
        dish_list = Dish.objects.filter(**search_dict)
        print(dish_list)
        if len(dish_list) == 0:
            dish_now = Dish.objects.create(dish_id=str(len(Dish.objects.all())+1), dish_name=dish_name, price=dish_price, description=dish_description, stall_id=user_id)
            dish_now.save()
        elif len(dish_list) == 1:
            dish_now = dish_list[0]
            dish_now.dish_name= dish_name
            dish_now.price = dish_price
            dish_now.description = dish_description
            dish_now.save()
        dish_list = Dish.objects.filter(stall_id=user_id)
    return render(request, 'shop/shop_dish.html', locals())


def shop_message(request):
    user_id = request.session.get('user_id', None)
    if user_id is not None:
        stall = Stall.objects.get(user_id=user_id)
        if stall is None:
            message = '您不是商家，请返回主页点餐'
        else:
            stall_id = stall.user_id
            if request.method == 'POST':
                name = request.POST.get('name')
                telephone = request.POST.get('telephone')
                address = request.POST.get('address')
                if len(name) != 0:
                    stall.name = name
                if len(address) != 0:
                    stall.address = address
                if len(telephone) != 0:
                    stall.telephone = telephone
                stall.save()
                message = '修改成功'
    return render(request, 'shop/shop_message.html', locals())