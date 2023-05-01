import pymysql

pymysql.install_as_MySQLdb()
pymysql.version_info = (1, 4, 13, "final", 0)

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
import re


# 用来验证用户是否有权限登陆的中间件
class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        url_path = request.path
        print(url_path)
        # 如果未登陆，则调转到登陆页面，将请求的url作为next参数
        if not request.user.is_authenticated:
            print('False')
            return redirect("/accounts/login/")

        # 如果已经登陆，则通过
        else:
            print('成功')
            return