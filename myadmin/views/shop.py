# 店铺信息管理的视图文件
import time
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils.crypto import random

from myadmin.models import User, Shop


def index(request, pIndex=1):
    # 浏览信息
    smod = Shop.objects
    slist = smod.filter(status__lt=9) # 状态码小于9 不显示
    mywhere = []
    # 获取并判断搜索条件
    kw = request.GET.get('keyword',None)
    if kw:
        # 查询店铺名称中只要含有关键字的都可以
        slist = slist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        slist = slist.filter(status=status)
        mywhere.append("status=" + status)
    # 分页处理
    pIndex = int(pIndex)
    page = Paginator(slist,5) # 每页显示5个
    maxpages = page.num_pages # 获得最大页数
    # 判断是否页数越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) # 获取当前页信息
    plist = page.page_range # 获取页码信息
    context = {'shoplist':list2,'plist':plist,'pIndex':pIndex,'mywhere':mywhere,'maxpages':maxpages}
    return render(request,'myadmin/shop/index.html',context)


def add(request):
    # 加载信息添加表单
    return render(request,"myadmin/shop/add.html")

def insert(request):
    # 执行信息添加
    try:
        # 店铺封面图片的上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse("没有店铺封面上传文件信息")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + cover_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 店铺logo图片的上传处理
        myfile = request.FILES.get("banner_pic", None)
        if not myfile:
            return HttpResponse("没有店铺logo上传文件信息")
        banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + banner_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()


        ob = Shop()
        ob.name = request.POST['name']
        ob.phone = request.POST['phone']
        ob.address = request.POST['address']
        ob.cover_pic = cover_pic
        ob.banner_pic = banner_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "添加成功！"}
    except Exception as err:
        print(err)
        context = {"info": "添加失败"}
    return render(request, "myadmin/info.html", context)


def delete(request,sid= 0):
    # 执行信息删除
    try:
        ob = Shop.objects.get(id=sid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "删除成功！"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败"}
    return render(request, "myadmin/info.html", context)


def edit(request,sid = 0):
    # 加载信息编辑表单
    try:
        ob = Shop.objects.get(id=sid)
        context = {"shop": ob }
        return render(request,'myadmin/shop/edit.html',context)
    except Exception as err:
        print(err)
        context = {"info": "没有找到修改的信息"}
        return render(request, "myadmin/info.html", context)


def update(request,sid):
    # 执行信息编辑
    try:
        ob = Shop.objects.get(id=sid)
        ob.name = request.POST['name']
        ob.phone = request.POST['phone']
        ob.address = request.POST['address']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": '修改成功！'}
    except Exception as err:
        print(err)
        context = {"info": "修改失败！"}
    return render(request, "myadmin/info.html", context)