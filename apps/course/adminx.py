# -*- encoding: utf-8 -*-
"""
@version: 0.1
@author: ferdinand
@flie: adminx.py
@ide: PyCharm
@time: 2018/6/8 15:00
"""

import xadmin
from xadmin import views

from .models import Course, Lesson, Video, CourseResource


class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = '黄祥的后台管理界面'
    site_footer = '黄祥的python_django学习'
    menu_style = 'accordion'


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)


class CourseAdmin(object):
    """课程"""
    list_display = ['name', 'dict', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'degree', 'learn_times', 'students']


class LessonAdmin(object):
    """章节"""
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    """视频"""
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


# 将管理器与model进行关联注册
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
