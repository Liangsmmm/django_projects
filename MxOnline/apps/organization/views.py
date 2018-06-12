# -*- encoding:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View

from django.http import HttpResponse, JsonResponse

from organization.models import CourseOrg, CityDict, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from organization.forms import UserAskForm
from operation.models import UserFavorite
from course.models import Course
from json import dumps
from django.db.models import Q
# Create your views here.

# 课程机构列表功能
class OrgListView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_city = CityDict.objects.all()
        key_word = request.GET.get('keywords', '')
        if key_word:
            all_orgs = all_orgs.filter(
                Q(name__icontains=key_word) | Q(desc__icontains=key_word) )


        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = CourseOrg.objects.filter(city_id=int(city_id))

        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category = category)
        sort = request.GET.get('sort', '')
        if sort == "students":
            all_orgs=all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs=all_orgs.order_by("-course_num")
        else:
            sort = ''


        org_nums = all_orgs.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 3, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs':orgs,
            'all_city':all_city,
            'org_nums':org_nums,
            'category':category,
            'city_id':city_id,
            'hot_orgs':hot_orgs,
            'sort':sort,
        })

    def post(self):
        pass


class UserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask = userask_form.save(commit = True)
            return  HttpResponse('{"status":"successful"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id = int(org_id))
        course_org.click_nums+=1
        course_org.save()
        courses = course_org.course_set.all()[:2]
        teschers = course_org.teacher_set.all()[:1]
        has_fav = False
        if UserFavorite.objects.filter(user = request.user, fav_id=int(course_org.id), fav_type=2):
            has_fav=True
        return render(request, "org-detail-homepage.html", {
            "courses": courses,
            "teachers": teschers,
            "course_org": course_org,
            "current_page": current_page,
            'has_fav':has_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        courses = course_org.course_set.all()
        has_fav=False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=int(course_org.id)):
            has_fav = True
        return render(request, "org-detail-course.html", {
            "courses": courses,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=int(course_org.id)):
            has_fav = True
        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id = int(org_id))
        has_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=int(course_org.id)):
            has_fav = True
        teschers = course_org.teacher_set.all()
        return render(request, "org-detail-teachers.html", {

            "teachers": teschers,
            "course_org": course_org,
            "current_page":current_page,
            "has_fav":has_fav,
        })


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated():
            return HttpResponse(dumps({'status':'fail', 'msg':'用户未登录'}), content_type="application/json")
        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_record:
            exist_record.delete()
            if(int(fav_type)==1):
                course=Course.objects.get(id=int(fav_id))
                course.fav_nums-=1
                if course.fav_nums<0:
                    course.fav_nums=0
                course.save()
            if(int(fav_type)==2):
                course_org=CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums-=1
                if course_org.fav_nums<0:
                    course_org.fav_nums=0
                course_org.save()
            if(int(fav_type)==3):
                teacher=Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums-=1
                if teacher.fav_nums<0:
                    teacher.fav_nums=0
                teacher.save()


            return HttpResponse(dumps({'status':'success','msg':'收藏'}), content_type="application/json")
        else:
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()

                if (int(fav_type) == 1):
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                if (int(fav_type) == 2):
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                if (int(fav_type) == 3):
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                # return HttpResponse(dumps({'status':'success','msg':'已收藏'}), content_type="application/json")
                return JsonResponse({'status':'success','msg':'已收藏'})

            else:
                # return HttpResponse({'status': 'fail', 'msg': '收藏出错'}, content_type="application/json")
                return HttpResponse(dumps({'status':'fail','msg':'收藏出错'}), content_type="application/json")


class TeacherView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()

        key_word = request.GET.get('keywords', '')
        if key_word:
            all_teachers = all_teachers.filter(
                Q(name__icontains=key_word) | Q(work_company__icontains=key_word))

        hot_teachers = all_teachers.all().order_by("-click_nums")[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)



        return render(request, "teachers-list.html", {
            "all_teachers":teachers,
            "hot_teachers":hot_teachers,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id = int(teacher_id))
        teacher.click_nums+=1
        teacher.save()
        teacher_courses = Course.objects.filter(teacher=teacher)
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        return render(request, "teacher-detail.html", {
            "teacher":teacher,
            "hot_teachers":hot_teachers,
            "teacher_courses":teacher_courses,
        })



