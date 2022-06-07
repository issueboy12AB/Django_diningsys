# 订单信息管理的视图文件
import os
import time

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from datetime import datetime
# Create your views here.
from myadmin.models import Category, Shop, Product, Orders, Member, User, OrderDetail


def index(request, pIndex=1):
    '''浏览信息'''
    umod = OrderDetail.objects
    olist = umod.filter( status__lt=9 )
    mywhere = []
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    if kw:
        olist = olist.filter(name__contains=kw)
        mywhere.append('keyword=' + kw)
    # 获取并判断搜索菜品类别条件
    oid = request.GET.get("order_id", '')
    if oid != '':
        olist = olist.filter(order_id=oid)
        mywhere.append('order_id=' + oid)
    # 获取、判断并封装状态status搜索条件
    pid = request.GET.get('product_id', '')
    if pid != '':
        olist = olist.filter(product_id=pid)
        mywhere.append("product_id=" + pid)

    # 执行分页处理
    olist = olist.order_by("id")  # 对id排序
    pIndex = int(pIndex)
    page = Paginator(olist, 5)  # 以每页5条数据分页
    maxpages = page.num_pages  # 获取最大页数
    # 判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息


    context = {"ordersdetaillist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/ordersdetail/index.html", context)
