# -*- encoding: utf-8 -*-
"""
@version: 0.1
@author: ferdinand
@flie: forms.py
@ide: PyCharm
@time: 2018/6/9 01:20
"""
from django import forms
from captcha.fields import CaptchaField


# 登录表单验证
class LoginForm(forms.Form):
    # 用户名密码不能为空
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


# 注册表单
class RegisterForm(forms.Form):
    """注册验证表单"""
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)

    # 验证码
    captcha = CaptchaField(error_messages={'invalid': '验证码错误！'})


# 忘记密码
class ForgetPwForm(forms.Form):
    """忘记密码"""
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})
