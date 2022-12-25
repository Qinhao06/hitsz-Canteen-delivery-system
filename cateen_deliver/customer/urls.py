from . import views

from django.urls import path
from .views import login, register, logout, change_password


app_name = 'customer'
urlpatterns = [
    path('change_password/', change_password),
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
    # path('show_info/', show_info, name='show_info'),

]