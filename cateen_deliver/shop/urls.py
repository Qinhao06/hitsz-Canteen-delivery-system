from django.http import HttpResponse


from django.urls import path

from . import admin
from .views import shop_manage, shop_dish, shop_order, shop_message

urlpatterns = [
    path('', shop_manage, name="shopManage"),
    path('dish/', shop_dish),
    path('order/', shop_order),
    path('message/', shop_message)
]