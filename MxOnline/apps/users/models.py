# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=20, verbose_name=u"昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(choices=(("male",u"男"),("female",u"女")), default="female", max_length=10, verbose_name=u"性别")
    address = models.CharField(max_length=100, verbose_name=u"地址", default=u"")
    mobile = models.CharField(max_length=11, verbose_name=u"手机号", null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y/%m", max_length=100, verbose_name=u"头像", default=u"image/default")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def get_unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    email = models.EmailField(verbose_name=u"邮箱", max_length=50)
    code = models.CharField(verbose_name=u"验证码", max_length=20)
    send_type = models.CharField(choices=(("forget",u"找回密码"),("register",u"注册"),("update", u"修改邮箱")), default="register", max_length=20, verbose_name=u"验证类型")
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", max_length=100, verbose_name=u"轮播图", default=u"banner/default")
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

