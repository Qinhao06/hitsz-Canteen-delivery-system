from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from .form import LoginForm, RegisterForm
from django.contrib import messages
from dish.models import Customer, Userinfo


def login(request):
    if request.session.get('is_login', None):
        print("[DEBUG][POST][STATE]:已经登陆")
        return render(request, 'base.html', locals())

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # identy 表示
            print("[DEBUG][POST][LOGIN][username]:{}".format(username))
            print("[DEBUG][POST][LOGIN][password]:{}".format(password))
            try:
                print("[DEBUG][POST][STATE]:查询顾客用户数据库")
                user_cus = Userinfo.objects.get(user_id=username)
                if user_cus.password == password:
                    print("[DEBUG][POST][USERNAME]:{}登录成功".format(user_cus.user_id))
                    message = "登录成功,请前往主页点餐"
                    request.session['is_login'] = True
                    request.session['user_id'] = user_cus.user_id
                    user_cus.status = 1
                    user_cus.save()
                    success = 1
                    return render(request, 'customer/login.html', locals())
                else:
                    print("[DEBUG][POST][STATE]:密码不正确")
                    message = "密码不正确"
            except:
                print("[DEBUG][POST][STATE]:用户不存在")
                message = "用户不存在"
    return render(request, 'customer/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return render(request, 'customer/logout.html', locals())
    user_id = request.session['user_id']
    print("[DEBUG][REQUEST][退出]]")
    print("[DEBUG][REQUEST][USER_ID]:{}".format(user_id))
    try:
        user = Userinfo.objects.get(user_id=user_id)
        print("[DEBUG][REQUEST][退出]]：退出顾客身份")
        user.status = 0  # 更新离线状态
        user.save()
        message = '已经登出,请重新登录或注册'
    except:
        print("[DEBUG][request][STATE]:退出错误，无法更新数据库中用户状态")

    request.session.flush()
    return render(request, 'customer/logout.html', locals())


def change_password(request):
    if not request.session.get('is_login', None):
        print('[DEBUG][POST][STATE]:尚未登录，不能修改密码')
        message = "请先登录"
        return render(request, 'customer/login.html', locals())
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        cus_type = request.POST.get('type')
        print("[DEBUG][POST][LOGIN][username]:{}".format(username))
        print("[DEBUG][POST][LOGIN][password]:{}".format(password))
        print("[DEBUG][POST][LOGIN][type]:{}".format(cus_type))
        if password1 != password2:  # 判断两次密码是否相同
            print("[DEBUG][POST][STATE]:两次输入的密码不同！")
            message = "两次输入的密码不同！"
            return render(request, 'customer/change_password.html', locals())
        else:
            same_id_use = Userinfo.objects.filter(user_id=username)
            # same_id_mng = StoreManager.objects.filter(manager_name=username)
            if not same_id_use:  # 用户名唯一
                message = '顾客不存在'
                print("[DEBUG][POST][STATE]:顾客不存在！")
                return render(request, 'customer/register.html', locals())
            # 当一切都OK的情况下，修改密码
            else:
                try:
                    user = Userinfo.objects.get(user_id=username)
                    if user.password == password:
                        print("[DEBUG][POST][STATE]:修改用户{}的密码".format(username))
                        user.password = password1
                        if user.type == 3:
                            cus = Customer.objects.get(user_id=username)
                            cus.cus_type = cus_type
                            cus.save()
                        user.status = 0
                        user.save()
                        message = '密码修改成功,请重新登录'
                        return render(request, 'customer/login.html', locals())
                except:
                    print("[DEBUG][POST][STATE]:修改密码原密码错误")
                    message = "原密码错误"
                return render(request, 'customer/change_password.html', locals())
    return render(request, 'customer/change_password.html')


def register(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        print("[DEBUG]禁止重登录")
        return render(request, 'customer/base.html', locals())  # 自动跳转到首页
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        cus_type = request.POST.get('type')
        print("[DEBUG][POST][LOGIN][username]:{}".format(username))
        print("[DEBUG][POST][LOGIN][password]:{}".format(password1))
        print("[DEBUG][POST][LOGIN][type]:{}".format(cus_type))
        if password1 != password2:  # 判断两次密码是否相同
            print("[DEBUG][POST][STATE]:两次输入的密码不同！")
            message = "两次输入的密码不同！"
            return render(request, 'customer/register.html', locals())
        else:
            same_id_use = Userinfo.objects.filter(user_id=username)
            # same_id_mng = StoreManager.objects.filter(manager_name=username)
            if same_id_use:  # 用户名唯一
                message = '顾客用户名已经存在⚔🔫你要不要换一个'
                print("[DEBUG][POST][STATE]:用户名唯一！")
                return render(request, 'customer/register.html', locals())
            # 当一切都OK的情况下，创建新用户
            else:
                Type = 3
                if cus_type == '商家':
                    Type = 4
                    new_user = Userinfo.objects.create(user_id=username, password=password1, type=Type, status=0)
                    new_user.save()
                else:
                    new_user = Userinfo.objects.create(user_id=username, password=password1, type=Type, status=0)
                    new_user.save()
                    new_cus = Customer.objects.create(user_id=username, cus_type=cus_type)
                    new_cus.save()
                # 自动跳转到登录页面
                login_form = LoginForm()
                message = "注册成功！"
                print("[DEBUG][POST][STATE]:注册成功")
                return render(request, 'customer/login.html', locals())  # 自动跳转到登录页面

    return render(request, 'customer/register.html', locals())
