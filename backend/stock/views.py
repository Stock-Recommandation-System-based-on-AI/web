from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Stock
from bs4 import BeautifulSoup
from pykrx import stock
from datetime import date, timedelta, datetime
import requests

# 17시가 지나면 당일의 데이터를 불러온다. 17시 전이라면 전날의 데이터를 불러온다.
time_data = datetime.now().strftime("%H:%M:%S")
if int(time_data[:2]) > 16:
    d = 0
else:
    d = 1
today = (date.today() - timedelta(d)).strftime('%Y%m%d')


# pykrx 라이브러리에서는 주말날짜의 데이터를 지원하지 않는다. 주말인경우 금요일로 날짜를 맞춘다.
if date(int(today[:4]), int(today[4:6]), int(today[6:])).weekday() > 4:
    minus_day = date(int(today[:4]), int(today[4:6]), int(today[6:])).weekday() - 4
    
    today = (date.today() - timedelta(minus_day) - timedelta(d)).strftime('%Y%m%d')
# Create your views here.
def main_page(request):
    stocks = Stock.objects.all().order_by('-probability')[:3]
    context = {
        "stocks": stocks,
    }
    return render(request, 'stock/main_page.html', context)


def forecasts(request):
    if request.user.is_authenticated:
        stocks = Stock.objects.all().order_by('-probability')
        if 'q' in request.GET:
            query = request.GET.get('q')
            stocks = Stock.objects.all().filter(Q(name__contains=query) | Q(id__contains=query))
        if 'p' in request.GET:
            query = request.GET.get('p')
            stocks = Stock.objects.all().filter(position=query)
        paginator = Paginator(stocks, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
        }
        return render(request, 'stock/forecasts.html', context)
    else:
        return redirect('accounts:login')


def forecast_detail(request, stock_pk):
    stock_detail = get_object_or_404(Stock, pk=stock_pk)

    urls = 'https://finance.naver.com/item/news.nhn?code=' + stock_detail.id
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    res = requests.get(urls,headers=headers)
    soups = BeautifulSoup(res.text,'html.parser')
    iframe_urls = soups.find_all('iframe')[3:5]
    news_iframe_url = iframe_urls[0]['src']
    disclosure_iframe_url = iframe_urls[1]['src']

    #주식 뉴스정보 데이터
    urls = 'https://finance.naver.com' + news_iframe_url
    res = requests.get(urls, headers=headers)
    soups = BeautifulSoup(res.text, 'html.parser')
    tr_list = soups.select('html > body > div.tb_cont > table.type5 > tbody > tr')[:5]
    news = []
    for tr in tr_list:
        title = tr.find('td', {'class': 'title'}).text
        link = 'https://finance.naver.com' + tr.find('a', {'class': 'tit'}).get('href')
        report = tr.find('td', {'class': 'info'}).text
        date = tr.find('td', {'class':'date'}).text
        obj = {
            'title': title,
            'link': link,
            'report': report,
            'date': date,
        }
        news.append(obj)

    # 주식 공시정보 데이터
    urls = 'https://finance.naver.com' + disclosure_iframe_url
    res = requests.get(urls, headers=headers)
    soups = BeautifulSoup(res.text, 'html.parser')
    tr_list = soups.select('html > body > div.tb_cont > table.type6 > tbody.first > tr')
    disclosure = []
    for tr in tr_list:
        title = tr.find('td', {'class': 'title'}).text
        link = 'https://finance.naver.com' + tr.find('a', {'class': 'tit'}).get('href')
        report = tr.find('td', {'class': 'info'}).text
        date = tr.find('td', {'class':'date'}).text
        obj = {
            'title': title,
            'link': link,
            'report': report,
            'date': date,
        }
        disclosure.append(obj)

    # 주식 펀더멘탈 데이터
    df = stock.get_market_fundamental_by_date(today, today, stock_pk)
    stock_data = df.to_dict('records')

    # 주식 매매동향 데이터
    df = stock.get_market_trading_volume_by_date(today, today, stock_pk, detail=True)
    trading_data = df.to_dict('records')
    context = {
        'stock_detail': stock_detail,
        'news': news,
        'disclosure': disclosure,
        'stock_data': stock_data[0],
        'trading_data': trading_data[0],
    }
    return render(request, 'stock/forecast_detail.html', context)


def interest(request, stock_pk):
    user = request.user
    stock = get_object_or_404(Stock, pk=stock_pk)
    if stock.interest_users.filter(pk=user.pk).exists():
        stock.interest_users.remove(user)
        interested = False
    else:
        stock.interest_users.add(user)
        interested = True
    context = {
        'interested': interested,
    }
    return JsonResponse(context)