# -*- encoding:utf-8 -*-
from django.conf.urls import url, include
from django.views.generic import TemplateView

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendCodeView, UpdateEmailView, MyCourseView, FavOrgView, FavCourseView
from .views import FavTeacherView, MessageView


urlpatterns = [

    url(r'^info/$', UserInfoView.as_view(), name="user_info"),
    url(r'^upload/image/$', UploadImageView.as_view(), name="upload_image"),
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    url(r'^sendemail_code/$', SendCodeView.as_view(), name="sendemail_code"),
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),
    # 我收藏的机构
    url(r'^myfav/org/$', FavOrgView.as_view(), name="fav_org"),
    url(r'^myfav/course/$', FavCourseView.as_view(), name="fav_course"),
    url(r'^myfav/teacher/$', FavTeacherView.as_view(), name="fav_teacher"),
    url(r'^mymessage/$', MessageView.as_view(), name="mymessage"),
]
