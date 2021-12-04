from django.shortcuts import render
from django.http import HttpResponse

from store.models import OrderItem, Product


def hi(request):

    return HttpResponse('hi')
