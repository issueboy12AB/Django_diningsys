# 订单信息管理的视图文件
import os
import time

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from datetime import datetime
# Create your views here.
from myadmin.models import Category, Shop, Product, Orders, Member, User


def index(request, pIndex=1):
    '''浏览信息'''
    umod = Orders.objects
    olist = umod.filter( status__lt=9 )
    mywhere = []
    # 获取并判断搜索条件
    status = request.GET.get('status', '')
    if status != '':
        olist = olist.filter(status=status)
        mywhere.append("status=" + status)

    # 执行分页处理
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

    # 遍历当前菜品信息并封装对应的店铺和菜品类别信息
    for vo in list2:
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name
        uob = User.objects.get(id=vo.user_id)
        vo.username = uob.username

    context = {"orderslist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/orders/index.html", context)


def delete(request, oid=0):
    '''执行信息删除'''
    try:
        ob = Orders.objects.get(id=oid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "删除成功！"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败！"}
    return render(request, "myadmin/info.html", context)


def edit(request, oid=0):
    '''加载信息编辑表单'''
    try:
        ob = Orders.objects.get(id=oid)
        context = {'orders': ob}
        slist = Shop.objects.values("id", 'name')
        context["shoplist"] = slist
        ulist = User.objects.values("id", 'username')
        context["userlist"] = ulist
        return render(request, "myadmin/orders/edit.html", context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def update(request, oid):
    '''执行信息编辑'''
    try:
        ob = Orders.objects.get(id=oid)
        ob.shop_id = request.POST['shop_id']
        ob.user_id = request.POST['user_id']
        ob.money = request.POST['money']
        ob.status = request.POST['status']
        ob.payment_status = request.POST['payment_status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "修改成功！"}

    except Exception as err:
        print(err)
        context = {'info': "修改失败！"}

    return render(request, "myadmin/info.html", context)
