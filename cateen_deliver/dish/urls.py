from django.urls import path

from . import views

urlpatterns = [
    path('', views.dish, name="dish")
]


