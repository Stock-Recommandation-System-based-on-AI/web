from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm
from stock.models import Stock, Stock_price
from datetime import date, timedelta, datetime

# Create your views here.
# 17시가 지나면 당일의 데이터를 불러온다. 17시 전이라면 전날의 데이터를 불러온다.
time_data = datetime.now().strftime("%H:%M:%S")
if int(time_data[:2]) > 16:
    d = 0
else:
    d = 1
today = (date.today() - timedelta(d)).strftime('%Y-%m-%d')
# pykrx 라이브러리에서는 주말날짜의 데이터를 지원하지 않는다. 주말인경우 금요일로 날짜를 맞춘다.
if date(int(today[:4]), int(today[5:7]), int(today[8:])).weekday() > 4:
    minus_day = date(int(today[:4]), int(today[4:6]), int(today[6:])).weekday() - 4
    today = (date.today() - timedelta(minus_day) - timedelta(d)).strftime('%Y-%m-%d')


def post_list(request):
    posts = Post.objects.order_by('-pk')
    for post in posts:
        stock = Stock.objects.get(name=post.stock)
        today_price = Stock_price.objects.get(stock=stock.pk, date=today).price
        post.today_price = today_price
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'community/post_list.html', context)


def post_create(request):
    if request.user.is_authenticated:
        stocks = Stock.objects.all()
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                stock = Stock.objects.get(name=form.stock)
                stock_price = Stock_price.objects.get(stock=stock.pk, date=today)
                form.user = request.user
                form.current_price = stock_price.price
                form.save()
                return redirect('community:post_list')
        else:
            form = PostForm()

        context = {
            'stocks': stocks,
            'form': form,
            'positions': ['홀드','매수','매도']
        }
        return render(request, 'community/post_form.html', context)
    else:
        return redirect('accounts:login')


def post_detail(request, post_pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_pk)
        stock = Stock.objects.all().get(name=post.stock)
        today_price = Stock_price.objects.get(stock=stock.pk, date=today).price
        post.today_price = today_price
        context = {
            'post': post,
            'stock': stock,
        }
        return render(request, 'community/post_detail.html', context)
    else:
        return redirect('accounts:login')   


def post_update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user != post.user:
        return redirect('community:post_list')
    if request.method =="POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('community:post_detail', post_pk)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'community/post_form.html', context)


def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user != post.user:
        return redirect('community:post_list')
    post.delete()
    return redirect('community:post_list')
