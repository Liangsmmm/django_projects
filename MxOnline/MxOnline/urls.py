"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve




from users.views import UserLoginView, UserLogoutView, IndexView, RegisterView, ActiveUserView, ForgetPwdView, ModifyPwdView, ResetPwdView
from organization.views import OrgListView
from MxOnline.settings import MEDIA_ROOT
    # , STATIC_ROOT

import xadmin


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name="index"),
    url('^login/$', UserLoginView.as_view(), name="login"),
    url('^logout/$', UserLogoutView.as_view(), name="logout"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url('^captcha/', include('captcha.urls')),
    url('^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url('^forgetpwd/$', ForgetPwdView.as_view(), name="forgetpwd"),
    url('^reset/(?P<reset_code>.*)/$', ResetPwdView.as_view(), name="user_reset"),
    url('^modifypwd/$', ModifyPwdView.as_view(), name="modifypwd"),
    url(r'^org/', include('organization.urls', namespace="org")),
    url(r'^course/', include('course.urls', namespace="course")),
    url(r'^users/', include('users.urls', namespace="users")),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {"document_root":STATIC_ROOT}),

]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'