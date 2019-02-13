import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm.settings")
    import django
    django.setup()


    from app01 import models
    from django.core import serializers

    # 1.对于Django的Queryset < Queryset[object, object, object] >
    # 这种关于django的Querysetset对象这种是不能用python的json方法，这时候就需要用到django的serializers

    ret = models.Book.objects.all()
    print(ret,type(ret))

    data = serializers.serialize("json",ret)

    print(data,type(ret))
    

    #2、json.dumps
    import json

    #关于python一些内置一些类型（例如：字典，列表，元祖。。。）的序列化，就用json就可以了

    #只要不是关于django对象的序列化，就用json.dumps

    ret = models.Book.objects.all().values('title')  #得到的是字典QuerySet
    print(ret)
    # ret = models.Book.objects.all().values_list('title')
    #转换成列表
    ret = list(ret)
    print(ret)

    result = json.dumps(ret)
    print("===========")
    print(result)

