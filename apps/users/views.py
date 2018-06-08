from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwForm
from utils.email_send import send_register_email


# 邮箱和用户名都可以登录，基础类ModelBackend，因为其有authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个，两个是get失败都一种原因，Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))

            # django后台中密码加密：所以不能password=password
            # UserProfile继承都AbstractUser中有def check_password(self, raw_password)
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户提交的账号密码
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)

            # 成功返回user对象，失败None
            user = authenticate(username=user_name, password=pass_word)
            # 如果不是null则说明验证成功
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户名或者密码错误！', 'login_form': login_form})
        else:
            return render(request, 'login.html',  {'msg': '用户名或者密码错误！', 'login_form': login_form})


# 注册视图
class RegisterView(View):
    """用户注册"""
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm()
        if register_form.is_valid():
            user_name = request.POST.get('email', None)
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})
            pass_word = request.POST.get('password', None)
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name, 'register')


class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'login.html')
        else:
            return render(request, 'active_fail.html', {'msg': '您的激活链接无效！'})


class ForgetPwView(View):
    """找回密码"""
    def get(self, request):
        forget_form = ForgetPwForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

