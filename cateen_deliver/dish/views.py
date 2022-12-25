from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Dish


def dish(request):
    dishs = Dish.objects.all()
    return render(request, './base.html', locals())


