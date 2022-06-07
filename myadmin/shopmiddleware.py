from django.shortcuts import redirect
from django.urls import reverse

import re

class ShopMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        print('ShopMiddleware')
        # One-time configuration and initialization.

    def __call__(self, request):
        path = request.path
        print('url:',path)

        # 后台请求路由判断
        # 定义网站后台不用登录也可访问的路由url
        urllist = ['/myadmin/login/','/myadmin/dologin/','/myadmin/logout/','/myadmin/verify/']
        # 判断当前请求是否是访问网站后台,并且path不在urllist中
        if re.match(r'^/myadmin',path) and (path not in urllist):
            # 判断当前用户是否没有登录
            if 'adminuser' not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('myadmin_login'))

        #判断大堂点餐请求的判断，判断是否登录（session中是否有webuser）
        if re.match(r'^/web',path):
            #判断是否登录(在于session中没有webuser)
            if 'webuser' not in request.session:
                #重定向到登录页
                return redirect(reverse("web_login"))

        # 移动端请求路由判断
        # 定义移动端不用登录也可访问的路由url
        urllist = ['/mobile/register/', '/mobile/doregister/']
        # 判断当前请求是否是访问移动端,并且path不在urllist中
        if re.match(r'^/mobile', path) and (path not in urllist):
            # 判断当前用户是否没有登录
            if 'mobileuser' not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('mobile_register'))

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response