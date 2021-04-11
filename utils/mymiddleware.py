from django.utils.deprecation import MiddlewareMixin

from sales import models
from  django.shortcuts import redirect,reverse,HttpResponse,render
import re

class UserAuth(MiddlewareMixin):
    witle_list = [reverse('register'),reverse('login'),reverse('get_valid_img'),'/admin/']
    def process_request(self,request):

        #白名单放行
        for url in self.witle_list:
            # print(url,request.path)
            if re.match(url,request.path):
                return
        # if request.path in self.witle_list:
        #     return

        #登录认证
        user_obj = models.UserInfo.objects.filter(pk=request.session.get('user_id')).first()
        print('>>>>>:', user_obj, request.session.get('user_id'))
        request.obj = user_obj
        if user_obj is None:
            return redirect('login')

        # user_obj = models.UserInfo.objects.filter(pk=request.session.get('user_id')).first()
        # print('>>>>>:', user_obj, request.session.get('user_id'))
        # request.obj = user_obj
        # if user_obj:
        #     print('登陆成功')
        #     return
        # else:
        #     return redirect('login')
        #

        #权限认证
        #权限认证
        permissions = request.session.get('permissions')
        for permission in permissions:
            print(permission['permissions__url'],request.path)
            if re.match(permission['permissions__url'],request.path):
                print(re.match(permission['permissions__url'],request.path),re.match(permission['permissions__url'],request.path).group())
                return
        else:
            return HttpResponse('权限不足')





    def process_response(self,request,response):

        return response