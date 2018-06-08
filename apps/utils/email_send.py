# -*- encoding: utf-8 -*-
"""
@version: 0.1
@author: ferdinand
@flie: email_send.py
@ide: PyCharm
@time: 2018/6/9 02:24
"""
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from online_edu_platform.settings import EMAIL_FROM


# 生成随机字符串
def random_str(random_length=8):
    my_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        my_str += chars[random.randint(0, length)]
    return my_str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '黄祥的在线教育平台注册激活链接'
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass
