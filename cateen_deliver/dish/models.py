# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Canteen(models.Model):
    canteen_id = models.CharField(primary_key=True, max_length=10, verbose_name="食堂编号")
    canteen_manager = models.ForeignKey('CanteenManager', models.DO_NOTHING, blank=True, null=True, verbose_name="食堂管理员")
    canteen_address = models.TextField(blank=True, null=True, verbose_name="食堂地址")
    canteen_name = models.TextField(blank=True, null=True, verbose_name="食堂名称")
    hygiene_rating = models.IntegerField(blank=True, null=True, verbose_name="卫生等级")

    class Meta:
        ordering = ['canteen_id']
        db_table = 'canteen'
        verbose_name = "食堂"
        verbose_name_plural = "食堂"


class Dish(models.Model):
    dish_id = models.CharField(primary_key=True, max_length=10, verbose_name="菜品编号")
    dish_name = models.CharField(max_length=10, blank=True, null=True, verbose_name= "菜品名称")
    stall = models.ForeignKey('Stall', models.DO_NOTHING, blank=True, null=True, verbose_name="菜品商家")
    price = models.IntegerField(blank=True, null=True, verbose_name="菜品价格")
    description = models.TextField(blank=True, null=True, verbose_name="菜品描述")

    class Meta:
        ordering = ['dish_id']
        db_table = 'dish'
        verbose_name = "菜品"
        verbose_name_plural = verbose_name


class Stall(models.Model):
    user = models.OneToOneField('Userinfo', models.DO_NOTHING, primary_key=True, verbose_name="商家编号")
    canteen = models.ForeignKey(Canteen, models.DO_NOTHING, blank=True, null=True, verbose_name="商家所属食堂")
    name = models.TextField(blank=True, null=True, verbose_name="商家名称")
    telephone = models.TextField(blank=True, null=True, verbose_name="电话")
    address = models.TextField(blank=True, null=True, verbose_name="地址")

    class Meta:
        # ordering = ['user']
        db_table = 'stall'
        verbose_name = "商家"
        verbose_name_plural = verbose_name


class Orders(models.Model):
    order_id = models.CharField(primary_key=True, max_length=10, verbose_name="订单编号")
    user = models.ForeignKey('Customer', models.DO_NOTHING, verbose_name="顾客", default='')
    dish = models.ForeignKey(Dish, blank=True, null=True, verbose_name="菜品编号", default="-1", on_delete=models.CASCADE,)
    dish_num = models.IntegerField(blank=True, null=True, verbose_name="菜品数量")
    order_status = models.IntegerField(blank=True, null=True, verbose_name="订单状态")
    address = models.TextField(blank=True, null=True, verbose_name="外送地址")
    telephone = models.CharField(max_length=10, blank=True, null=True, verbose_name="联系方式")
    order_time = models.DateTimeField(verbose_name="下单时间")

    class Meta:
        ordering = ['order_id'];
        db_table = 'orders'
        verbose_name = "订单"
        verbose_name_plural = verbose_name


class Userinfo(models.Model):
    user_id = models.CharField(primary_key=True, max_length=10, verbose_name="用户id")
    password = models.CharField(max_length=10, verbose_name="用户密码")
    type = models.IntegerField(verbose_name="用户类型")
    status = models.IntegerField(choices=[(0, '离线'), (1, '在线')], default=0, verbose_name="顾客状态")

    class Meta:
        ordering = ['user_id']
        db_table = 'userinfo'
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Assessment(models.Model):
    assessment_id = models.CharField(primary_key=True, max_length=10, verbose_name="评价编号")
    order = models.ForeignKey(Orders, blank=True, null=True, verbose_name="订单编号", on_delete=models.CASCADE)
    score = models.IntegerField(blank=True, null=True, verbose_name="分数")
    assessment_time = models.DateTimeField(blank=True, null=True, verbose_name="评价时间")
    context = models.TextField(blank=True, null=True, verbose_name="评价内容")

    class Meta:
        ordering = ['assessment_id']
        db_table = 'assessment'
        verbose_name = "评价"
        verbose_name_plural = verbose_name


class Customer(models.Model):
    user = models.OneToOneField(Userinfo, primary_key=True, verbose_name="顾客", on_delete=models.CASCADE)
    cus_type = models.TextField(blank=True, null=True, verbose_name="顾客姓名")

    class Meta:
        # ordering = ['user']
        db_table = 'customer'
        verbose_name = "顾客"
        verbose_name_plural = verbose_name


class CanteenManager(models.Model):
    user = models.OneToOneField('Userinfo', models.DO_NOTHING, primary_key=True, verbose_name="食堂管理员")
    telephone = models.TextField(blank=True, null=True, verbose_name="电话")

    class Meta:
        # ordering = ['user']
        db_table = 'canteen_manager'
        verbose_name = "食堂管理员"
        verbose_name_plural = verbose_name
