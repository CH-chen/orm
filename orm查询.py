import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm.settings")
    import django
    django.setup()

    from app01 import models
    #单表查询
    book_obj = models.Book.objects.all()   #输出对象列表
    print(book_obj)
    for book in book_obj:
        print(book.title)
    print("=======")
    ret = models.Book.objects.values('title')  #输出字典形式的对象列表queryset
    print(ret)
    for i in ret:

        print(i["title"])
        # print(i["price"])
        print("&&&&&&&&&&")
    ret = models.Book.objects.values_list('title', 'price')  # 输出元祖形式的对象列表queryset
    print(ret)
    for i in ret:
        print(i[0])  #打印所有书籍的名字
        print(i[1]) #打印所有价格
    print("======================")

    #跨表查询  一对多
    #查询第一本书的出版社的名字 ----------- 查询语法格式：对象.关联字段.字段名
    ret = book_obj.first().publish.name
    print(ret)
    #查询所有书籍对应出版社的名字 -----------查询语法格式：关联字段__字段名
    ret = models.Book.objects.values("title","publish__name")
    print(ret)
    for i in ret:
        print(i["title"]) #打印所有书籍的名字
    #反向查询 查询第一个出版社出的书籍的名称

    publish_obj = models.Publish.objects.first()
    books = publish_obj.book_set.all()  #一个出版社有多本书，是一个列表对象
    print(books.values("title"))
    #查询所有出版社对应出的书的名字 -----------语法：表名__字段
    ret = models.Publish.objects.values("name","book__title")
    print(ret)
    #查询北京出版社所出的书  正向查询
    ret = models.Book.objects.filter(publish__name="北京出版社").values("title")
    print(ret)
    print("+++++++++++")
    #反向查询
    ret = models.Publish.objects.filter(name="北京出版社").values("book__title")
    print(ret)
    # 跨表查询  一对一
    #正向查询   ------- 查询语法格式：对象.关联字段.字段名
    author_obj = models.Author.objects.first()
    ret = author_obj.authorDetail.telephone
    print(ret)
    #反向查询 ------- 查询语法格式：对象.表名.字段名
    authordetail_obj = models.AuthorDetail.objects.first()
    ret = authordetail_obj.author.name
    print(ret)
    #查询所有作者的电话
    author_list = models.Author.objects.all()
    for i in author_list:
        print(i.authorDetail.addr)
    authordetail_list = models.AuthorDetail.objects.all()
    for i in authordetail_list:
        print(i.author.name)
    ret = models.Author.objects.values("authorDetail__telephone")
    for i in ret:
        print(i["authorDetail__telephone"])
    ret = models.AuthorDetail.objects.values("author__name")
    print(ret)
    for i in ret:
        print(i["author__name"])
    print("&&&&&&&&&&")

    #多对多查询

    #查询书名为web对应的作者
    book_list = models.Book.objects.filter(title="web").first() #取的是单个的对象
    ret = book_list.authors.all()
    print(ret)
    for name_list in ret:
        print(name_list.name,name_list.authorDetail.telephone)

    #查询所有书籍对应的作者
    book_list = models.Book.objects.all()
    for book_obj in book_list:  #取出单个的对象，单个对象对应多个，相当于一对多查询
        ret = book_obj.authors.all()
        for name_list in ret:
            print(book_obj.title,name_list.name,name_list.authorDetail.telephone)
    print("\\\\\\\\\\\\===========")
    author_list = models.Author.objects.all()
    for author_obj in author_list:
        # 取出单个的对象，单个对象对应多个，相当于一对多查询
        ret = author_obj.book_set.all()
        print(ret.values("title"))
        for i in ret:
            print(i.title)

    print("\\\\\\\\\\\\")

    # 查询所有书籍对应的作者 双下划线查询
    ret = models.Book.objects.values("title","authors__name")
    print(ret)
    for name_list in ret:
        print(name_list["title"],name_list["authors__name"])

    #查询小明出的书籍
    ret = models.Book.objects.filter(authors__name="小明").values("title")
    print(ret)
    #反向查询
    ret = models.Author.objects.filter(name="小明").values("book__title")
    print(ret)
    print("跨三张表查询")
    #书籍为web的作者的电话
    ret = models.Book.objects.filter(title="web").values("authors__name","authors__authorDetail__telephone")
    print(ret)
    ret = models.Author.objects.filter(book__title="web").values("authorDetail__telephone")
    print(ret)
    #查询第一个出版社出版书籍的作者
    ret = models.Publish.objects.first().book_set.all().values("authors__name")
    print(ret)
    ret = models.Book.objects.filter(publish__pk=1).values("authors__name")
    print(ret)
    #跨四个表查询
    # 查询第一个出版社出版书籍的作者的电话
    ret = models.Publish.objects.first().book_set.all().values("authors__authorDetail__telephone")
    print(ret)
    ret = models.Book.objects.filter(publish__pk=1).values("authors__authorDetail__telephone")
    print(ret)
    #查询第一个出版社出版书籍的详情列表
    publish_obj = models.Publish.objects.filter(pk=1).first()
    book = publish_obj.book_set.all()
    ret = models.AuthorDetail.objects.filter(author__nid=publish_obj.book_set.all())
    print('*************')
    #只取某几列query=[{},{},{}]里面是字典
    ret = models.Book.objects.all().values('title','price')
    for i in ret:
        print(i["title"])
        # print(i["price"])
        print("&&&&&&&&&&")
    #query=[(),(),()]里面是元祖
    ret = models.Book.objects.values_list('title', 'price')
    print(ret)
    for i in ret:
        print(i[0])  # 打印所有书籍的名字
        print(i[1])  # 打印所有价格
    print("======================")
    #query=[obj，obj]里面是对象
    ret = models.Book.objects.all().only('title','price')#only里面的字段最好和下面的对应，要不然性能会降低
    for item in ret:
        print(item.title,item.price,item.publishDate)#加上publishDate会降低性能
    ret = models.Book.objects.all().defer('title','price')#排除里面的字段

    print(ret)
    for item in ret:
        print(item.nid,item.title,)
        print('&&&&&&&&&')
        print(item.title,item.price)

    ret = models.Book.objects.all()
    for item in ret:
        print(item.title,item.publish.city)#这样写会跨表，性能会降低
    # 性能相关 select_related和prefetch_related比object.all()性能高，一般用select_related
    #如果有foreignkey 或者onetoone可以用select_related，可以提高性能
    ret = models.Book.objects.all().select_related('publish')#主动创建关联关系,一次链表，如果链表多，性能会差
    print('\\\\\\\\\\\\\\')
    for item in ret:
        print(item.title,item.publish.city)

    ret = models.Book.objects.all().prefetch_related('publish')  # 二次单表查询
    print('|||||||||||||||')
    for item in ret:
        print(item.title, item.publish.city)

    print("@@@@@@@@@@@")
    ret = models.Publish.objects.filter(nid__in=[1,3,4])
    print(ret)
    ret =models.Publish.objects.exclude(nid__in=[1,4])
    print(ret)
    ret = models.Publish.objects.filter(nid__gt=1,nid__lt=4)  #大于1小于4
    print(ret)
    ret = models.Publish.objects.filter(nid__gte=1,nid__lte=3) #大于等于1小于等于3
    print(ret)

    ret = models.Publish.objects.filter(name__contains="北京")
    print(ret)
    ret = models.Publish.objects.filter(name__icontains="北京")
    print(ret)
    ret = models.Publish.objects.filter(nid__range=[1,3])
    print(ret)
    ret = models.Publish.objects.all().order_by("nid").reverse()
    print(ret)


    ##########   聚合 ##############
    from django.db.models import Avg,Sum,Max,Min,Count
    ret = models.Book.objects.all().aggregate(Avg("price"))
    print(ret)
    ret = models.Book.objects.all().aggregate(avg_price=Avg("price"))
    print(ret)
    ret = models.Book.objects.all().aggregate(Avg("price"),Sum("price"),Max("price"),Min("price"))
    print(ret)
    ret = models.Publish.objects.annotate(avg=Avg("book__price")).values("name","avg")
    print(ret)

    #################-----F和Q-----###########

    #F()来做这样的比较查

    from django.db.models import F,Q
    #询评论数大于收藏数的书籍
    models.Book.objects.filter(commnet_num__gt=F('keep_num'))
    #将每一本书的价格提高30元
    models.Book.objects.all().update(price=F("price") + 30)

    #查询作者名是aaa或bbb的
    models.Book.objects.filter(Q(authors__name="aaa") | Q(authors__name="bbb"))
    #查询出版年份是2017或2018，书名中带经济的所有书。
    models.Book.objects.filter(Q(publish_date__year=2018) | Q(publish_date__year=2017), title__icontains="经济")