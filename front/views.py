from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.template.loader import render_to_string
from datetime import datetime
from django.db import connection
from .models import Film
from .models import Tag
from .models import Region
import pandas as pd


class Person(object):
    def __init__(self, username):
        self.username = username


def index(request):
    # ?username=xxx
    connection_mysql_db(request)
    username = request.GET.get('username')
    context = {
        'username': username,
        "today": datetime.now()
    }
    if username:
        # html = render_to_string("base.html")
        # return HttpResponse(html)
        return render(request, 'index.html', context=context)
    else:
        # 多个app中出现同名url，使用应用命名空间解决冲突问题
        login_url = reverse('front:login')
        return redirect(login_url)


def login(request):
    return render(request, 'signin.html')


def get_cursor():
    return connection.cursor()


def book(request):
    # # 1. 使用ORM添加一条数据到数据库中
    # book = Book(name='三国演义', author='罗贯中', price=200)
    # book.save()

    # 2. 查询
    # 2.1 根据主键进行查找
    # book = Book.objects.get(id=2)
    # print(book)
    # 2.2 根据其他条件进行查找
    # books = Book.objects.filter(name='西游记').first()
    # print(books)

    # 3. 删除数据
    # book = Book.objects.get(pk=1)
    # book.delete()

    # 4. 修改数据
    # book = Book.objects.get(pk=2)
    # book.price = 200
    # book.save()

    try:
        cursor = get_cursor()
        try:
            cursor.execute("select * from book")
            books = cursor.fetchall()
            cursor.close()
            return render(request, 'book.html', context={'books': books})
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)


def add_movie():
    df = pd.read_csv('E:/WebSpider/2017films.csv', encoding='gbk')
    for row in df.iterrows():
        name = row[1]['mname']
        tags = row[1]['tag'].split(',')
        length = row[1]['mlength']
        releaseday = row[1]['releaseday']
        regions = row[1]['region'].split('/')
        boxoffice_tot = row[1]['boxoffice_tot']

        film = Film(name=name, length=length,
                    releaseday=datetime.strptime(releaseday, '%Y-%m-%d'),
                    boxoffice_tot=int(boxoffice_tot))
        film.save()

        for re in regions:
            r = Region(name=re)
            try:
                r.save()
                film.regions.add(r)
            except:
                pass

        for tag in tags:
            t = Tag(name=tag)
            try:
                t.save()
                film.tags.add(t)
            except:
                pass

        film.save()


def movie(request):
    # 从url获取参数
    page_num = int(request.GET.get("page")) if request.GET.get("page") is not None else 1
    data_start = (page_num - 1) * 10
    date_end = page_num * 10
    all_films = Film.objects.all()[data_start:date_end]

    # 每页显示多少数据
    per_page = 10
    # 总数据是多少
    total_count = Film.objects.all().count()
    # 需要多少页展示
    total_page, m = divmod(total_count, per_page)
    if m:
        total_page += 1

    html_str_list = []
    for i in range(1, total_page + 1):
        tmp = '<li><a href="/movie/?page={0}">{0}</a></li>'.format(i)
        html_str_list.append(tmp)

    page_html = "".join(html_str_list)
    return render(request, 'movie.html', {"films": all_films, "page_html": page_html})


def city(request):
    return render(request, 'city.html')


def for_test(request):
    context = {
        'person': {
            'username': 'MiracleShadow',
            'age': 21,
            'height': 180
            # 不能使用'keys', 'values'这样的可能产生歧义的属性
            # 因为访问一个字典的key对应的value，只能通过'字典.keys'的方式进行访问
            # 列表、元组同理
        },
        'persons': [
            '张三',
            '李四',
            '王五'
        ],
        'books': [
            {
                'name': '三国演义',
                'author': '罗贯中',
                'price': 100
            },
            {
                'name': '水浒传',
                'author': '施耐庵',
                'price': 99
            },
            {
                'name': '西游记',
                'author': '吴承恩',
                'price': 150
            },
            {
                'name': '红楼梦',
                'author': '曹雪芹',
                'price': 200
            },
        ]
    }
    return render(request, 'for_test.html', context=context)


def if_test(request):
    # p = Person('MiracleShadow')
    context = {
        # 'person': p,
        'person': {
            'username': 'MiracleShadow',
            'age': 21,
            'height': 180
            # 不能使用'keys', 'values'这样的可能产生歧义的属性
            # 因为访问一个字典的key对应的value，只能通过'字典.keys'的方式进行访问
            # 列表、元组同理
        },
        'persons': [
            '张三',
            '李四',
            '王五'
        ],
    }
    return render(request, 'if_test.html', context=context)


def add_view(request):
    context = {
        'value1': ['1', '2', '3'],
        'value2': [4, 5, 6],
    }
    return render(request, 'add.html', context=context)


def cut_view(request):
    return render(request, 'cut.html')


def date_view(request):
    context = {
        "today": datetime.now(),
    }
    return render(request, 'date.html', context=context)


def company(request):
    return render(request, 'company.html')


def school(request):
    return render(request, 'school.html')


def connection_mysql_db(request):
    cursor = connection.cursor()
    cursor.execute("show tables")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    return render(request, 'index.html')
