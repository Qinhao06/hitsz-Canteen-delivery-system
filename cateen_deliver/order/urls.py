from django.http import HttpResponse


from django.urls import path
from .views import order, payment, ass

urlpatterns = [
    path('', order, name="order"),
    path('payment/', payment, name='payment'),
    path('ass/', ass),
]