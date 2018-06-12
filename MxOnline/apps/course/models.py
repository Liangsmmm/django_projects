# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
# Create your models here.
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField


class Course(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构", default="")
    name = models.CharField(max_length=100, verbose_name=u"课程名")
    desc = models.CharField(max_length=200, verbose_name=u"课程描述")
    detail = UEditorField(verbose_name=u"课程详情",width=600, height=300, imagePath="courses/ueditor/",filePath="courses/ueditor/", default="")
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", default="", null=True, blank=True)
    degree = models.CharField(choices=(('cj',u"初级"),('zj',u"中级"),('gj',u"高级")), default="cj", max_length=10, verbose_name=u"难度等级")
    learn_times = models.IntegerField(verbose_name=u"学习时长（分钟）", default=0)
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", max_length=100, verbose_name=u"封面", default=u"courses/default")
    clicks_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    tag = models.CharField(max_length=200, verbose_name=u"课程标签", default="", null=True, blank=True)
    category = models.CharField(max_length=200, verbose_name=u"课程类别", default=u"后端开发", null=True, blank=True)
    course_know = models.CharField(max_length=200, verbose_name=u"课程须知", default="", null=True, blank=True)
    teacher_advice = models.CharField(max_length=200, verbose_name=u"讲师建议", default="", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_nums(self):
        return self.lesson_set.all().count()

    def get_learn_user(self):
        return self.usercourse_set.all()

    def get_lessons(self):
        return self.lesson_set.all()

    def get_resource(self):
        return self.courseresource_set.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    url = models.CharField(max_length=100, verbose_name=u"视频地址", null=True, blank=True, default="")
    learn_times = models.IntegerField(verbose_name=u"学习时长（分钟）", default=0, null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    download = models.FileField(max_length=100, upload_to="course/resource/%Y/%m", verbose_name=u"下载链接")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

