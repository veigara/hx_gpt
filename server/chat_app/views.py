from django.shortcuts import render,HttpResponse

# Create your views here.


def hello(request):     # 默认传参request
    return HttpResponse('hello')