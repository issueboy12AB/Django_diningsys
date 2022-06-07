# 员工信息管理的视图文件
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils.crypto import random

from myadmin.models import User, Member


def index(request, pIndex=1):
    # 浏览信息
    umod = Member.objects
    ulist = umod.filter(status__lt=9) # 状态码小于9 不显示
    mywhere = []
    # 获取、判断并封装状态mobile搜索条件
    mobile = request.GET.get('mobile', '')
    if mobile != '':
        ulist = ulist.filter(mobile__contains=mobile)
        mywhere.append("mobile=" + mobile)
    # 分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist,5) # 每页显示5个
    maxpages = page.num_pages # 获得最大页数
    # 判断是否页数越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) # 获取当前页信息
    plist = page.page_range # 获取页码信息
    context = {'memberlist':list2,'plist':plist,'pIndex':pIndex,'mywhere':mywhere,'maxpages':maxpages}
    return render(request,'myadmin/member/index.html',context)



def delete(request,uid= 0):
    # 执行信息删除
    try:
        ob = Member.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "删除成功！"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败"}
    return render(request, "myadmin/info.html", context)

