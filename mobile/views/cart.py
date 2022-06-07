from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.
from myadmin.models import User, Shop, Category, Product


def add(request):
    ''' 添加购物车操作 '''
    # 从session中获取名字为cartlist的购物车信息，若没有返回空{}
    cartlist = request.session.get('cartlist', {})
    # 获取菜品id
    pid = request.GET.get("pid",None)
    if pid is not None:
        # 从session中获取当前店铺的所有菜品信息，并从中获取要放入购物车的菜品
        product = Product.objects.get(id=pid).toDict()
        # 初始化当前菜品的购买量
        product['num'] = 1
        # 判断当前购物车中是否存在要放进购物车的菜品
        if pid in cartlist:
            cartlist[pid]['num'] += product['num'] # 增加购买量
        else :
            cartlist[pid] = product
        # 将cartlist购物车信息放入session中
        request.session['cartlist'] = cartlist
    # 跳转到首页
    return JsonResponse({'cartlist':cartlist})


def delete(request):
    ''' 删除购物车中商品操作 '''
    # 从session中获取名字为cartlist的购物车信息，若没有返回空{}
    cartlist = request.session.get('cartlist', {})
    # 获取菜品id
    pid = request.GET.get("pid", None)
    if pid is not None:
        # 删除cartlist中对应商品
        del cartlist[pid]
        # 将cartlist购物车信息放入session中
        request.session['cartlist'] = cartlist
    # 跳转到首页
    return JsonResponse({'cartlist':cartlist})



def clear(request):
    ''' 请空购物车操作 '''
    # 直接将session中cartlist购物车赋值{}
    request.session['cartlist'] = {}
    # 跳转到首页
    return JsonResponse({'cartlist':{}})


def change(request):
    ''' 更改购物车操作 '''
    # 从session中获取名字为cartlist的购物车信息，若没有返回空{}
    cartlist = request.session.get('cartlist', {})
    # 获取要修改商品的pid
    pid = request.GET.get('pid',0)
    # 获取要修改商品的num
    m = int(request.GET.get('num',1))
    if m < 1:
        m = 1
    # 更改cartlist中num
    cartlist[pid]['num'] = m
    # 将cartlist购物车信息放入session中
    request.session['cartlist'] = cartlist
    # 跳转到首页
    return JsonResponse({'cartlist':cartlist})
