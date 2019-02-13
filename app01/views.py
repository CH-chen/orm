from django.shortcuts import render,HttpResponse

# Create your views here.
from app01 import models
from django.core import serializers

def books_json(request):
    book_list = models.Book.objects.all()
    from django.core import serializers
    ret = serializers.serialize("json", book_list)
    for item in ret:
        print(item)
    return HttpResponse(ret)