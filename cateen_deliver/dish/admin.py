from django.contrib import admin

# Register your models here.

from .models import Canteen, Customer, CanteenManager, Orders, Userinfo, Stall, Dish

admin.site.register(Canteen)
admin.site.register(Userinfo)
admin.site.register(Orders)
admin.site.register(Stall)
admin.site.register(CanteenManager)
admin.site.register(Dish)
admin.site.register(Customer)
