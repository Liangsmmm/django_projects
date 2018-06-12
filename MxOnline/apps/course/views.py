# -*- encoding:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
from json import dumps
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Course, Lesson, Video, CourseResource
from operation.models import UserFavorite, CourseComment, UserCourse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all()




        key_word = request.GET.get('keywords', '')
        if key_word:
            all_courses = all_courses.filter(Q(name__icontains=key_word)|Q(desc__icontains=key_word)|Q(detail__icontains=key_word))
        all_courses = all_courses.order_by("-add_time")
        hot_courses = all_courses.order_by("-clicks_nums")[:3]
        sort = request.GET.get('sort', '')
        if sort == "students":
            all_courses = all_courses.order_by('-students')
        elif sort == "hot":
            all_courses = all_courses.order_by('-clicks_nums')
        else:
            sort = ""

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses":courses,
            "sort": sort,
            "hot_courses":hot_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        # course_id = request.GET.get('course_id','')
        course = Course.objects.get(id=int(course_id))
        course.clicks_nums += 1
        course.save()
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.id), fav_type=1):
                has_fav_course=True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.org.id), fav_type=2):
                has_fav_org=True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request, "course-detail.html", {
            "course":course,
            "relate_courses":relate_courses,
            "has_fav_course":has_fav_course,
            "has_fav_org":has_fav_org,
        })


class CourseVideoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id = int(course_id))
        course.students+=1
        course.save()
        # 查询是否用户和课程已经关联
        usercourse = UserCourse.objects.filter(course = course, user = request.user)
        if not usercourse:
            usercourse = UserCourse(user=request.user, course=course, message="")
            usercourse.save()


        resources = CourseResource.objects.filter(course=course)
        user_courses = UserCourse.objects.filter(course = course)
        user_ids = [user_course.user.id for user_course in user_courses]
        relate_user_courses  = UserCourse.objects.filter(user_id__in = user_ids)
        relate_courses = [relate_user_course.course for relate_user_course in relate_user_courses][:5]
        # relate_courses = [for user_id in ]



        return render(request, "course-video.html", {
            "course": course,
            "resources":resources,
            "relate_courses":relate_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id = int(course_id))
        # 查询是否用户和课程已经关联
        usercourse = UserCourse.objects.filter(course = course, user = request.user)
        if not usercourse:
            usercourse = UserCourse(user=request.user, course=course, message="")


        resources = CourseResource.objects.filter(course=course)
        course_comment = CourseComment.objects.filter(course=course)
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        relate_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        relate_courses = [relate_user_course.course for relate_user_course in relate_user_courses][:5]
        return render(request, "course-comment.html", {
            "course": course,
            "resources":resources,
            "course_comment":course_comment,
            "relate_courses": relate_courses,
        })


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(dumps({'status': 'fail', 'msg': u'用户未登录'}), content_type="application/json")

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', "")

        if int(course_id) > 0 and comments:
            course_comment  = CourseComment()
            course_comment.comments = comments
            course = Course.objects.get(id = int(course_id))
            course_comment.course = course
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse(dumps({'status':'success', 'msg':u'添加成功'}), content_type="application/json")

