# -*- encoding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from utils.mixin_utils import LoginRequiredMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from json import dumps
import json



from models import UserProfile, EmailVerifyRecord
from forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from course.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from users.models import Banner


# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username = username)|Q(email = username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserLoginView(View):
    def get(self, request):
        return render(request, 'login.html',{})
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg":u"用户未激活"})
            else:
                return render(request, "login.html", {"msg":u"用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form":login_form})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse("index"))


class IndexView(View):
    def get(self, request):
        banners = Banner.objects.all()[:5]
        course_banners = Course.objects.filter(is_banner=False)[:3]
        courses = Course.objects.filter(is_banner=False)[:6]
        orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {
            "banners":banners,
            "course_banners":course_banners,
            "courses":courses,
            "orgs":orgs,
        })


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response("404.html", {})
    response.status_code = 404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response("500.html", {})
    response.status_code = 500
    return response


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()

        return render(request, "register.html", {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email", "")

            if UserProfile.objects.filter(email=email):
                return render(request, "register.html", {"register_form":register_form, "msg":u"用户已经存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.password = make_password(pass_word)
            user_profile.email = email
            user_profile.is_active = False
            user_profile.save()
            send_register_email(email, "register")
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = u"欢迎您注册！"
            user_message.save()
            return render(request, "sendsuccess.html")
        else:
            return render(request, "register.html", {"register_form":register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code = active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email = email)
                user.is_active = True
                user.save()

        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ForgetPwdView(View):
    def get(self, request):

        forgetpwd_form = ForgetPwdForm()

        return render(request, "forgetpwd.html", {"forgetpwd_form":forgetpwd_form})
    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email', "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        return render(request, "login.html", {})


class ResetPwdView(View):
    def get(self, request, reset_code):
        all_record = EmailVerifyRecord.objects.filter(code = reset_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.filter(email = email)
                if user is not None:
                    # email = request.POST.get('password',"")


                    return render(request, "password_reset.html", {"email":email})
                else:
                    return render(request, "forgetpwd.html")

        else:
            return render(request, "active_fail.html")


        # all_record = EmailVerifyRecord.objects.filter(code = reset_code)
        # if all_record:
        #     for record in all_record:
        #         email = record.email
        #         user = UserProfile.objects.filter(email = email)
        #         if user is not None:
        #             pass_word = request.POST.get('password',"")
        #             user.password = make_password(pass_word)
        #             user.save()
        #             return render(request, "login.html")
        #         else:
        #             return render(request, "login.html")
        #
        # else:
        #     return render(request, "active_fail.html")


class ModifyPwdView(View):
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"modifypwd_form":modifypwd_form})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd1)
                user.save()
                return render(request, "login.html", {})
        return render(request, "password_reset.html",{})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "usercenter-info.html", {})
    def post(self, request):
        user_form = UserInfoForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponse(dumps('{"status":"success", "msg":u"信息修改成功"}'), content_type="application/json")
        else:
            return HttpResponse(dumps('{"status":"fail", "msg":u"信息验证失败"}'), content_type="application/json")


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            image_form.save()
            return HttpResponse(dumps('{"status":"success"}'), content_type="application/json")
        else:
            return HttpResponse(dumps('{"status":"fail"}'), content_type="application/json")


class UpdatePwdView(LoginRequiredMixin, View):
    def post(self, request):
        pwd_modify_form = ModifyPwdForm(request.POST)
        if pwd_modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse(dumps({'status': 'fail', 'msg': u'密码不一致'}), content_type="application/json")
            request.user.password = make_password(pwd1)
            request.user.save()
            return HttpResponse(dumps({'status': 'success', 'msg': u'修改密码成功'}), content_type="application/json")
        else:
            return HttpResponse(json.dumps(pwd_modify_form.errors), content_type="application/json")


class SendCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse(dumps({'status': 'fail', 'msg': u'邮箱已经存在'}), content_type="application/json")
        send_register_email(email, "update")
        return HttpResponse(dumps({'status': 'success', 'msg': u'验证码发送成功'}), content_type="application/json")


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        code = request.POST.get('code','')
        email = request.POST.get('email','')
        exist = EmailVerifyRecord.objects.filter(email=email, code=code)
        if exist:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse(dumps({'status': 'success', 'msg': u'邮箱修改成功'}), content_type="application/json")
        else:
            return HttpResponse(dumps({'status': 'fail', 'msg': u'邮箱验证失败'}), content_type="application/json")


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        usercourses = UserCourse.objects.filter(user = request.user)
        mycourses = []
        for usercourse in usercourses:
            mycourse = Course.objects.get(id=usercourse.course.id)
            mycourses.append(mycourse)
        return render(request, "usercenter-mycourse.html", {
            "mycourses":mycourses
        })


class FavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        fav_orgs = UserFavorite.objects.filter(fav_type=2, user=request.user)
        org_list = []
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            if CourseOrg.objects.filter(id=org_id):
                org = CourseOrg.objects.get(id=org_id)
                org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list":org_list
        })


class FavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        fav_courses = UserFavorite.objects.filter(fav_type=1, user=request.user)
        course_list = []
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            if Course.objects.filter(id=course_id):
                course = Course.objects.get(id=course_id)
                course_list.append(course)
        return render(request, "usercenter-fav-course.html", {
            "course_list":course_list
        })

        # fav_courses = UserFavorite.objects.filter(fav_type=1, user=request.user)
        # course_list = []
        # for fav_course in fav_courses:
        #     course_id = fav_course.fav_id
        #     course = Course.objects.get(id=fav_course.fav_id)
        #     if course:
        #         course_list.append(course)
        # return render(request, "usercenter-fav-course.html", {
        #     "course_list":course_list
        # })


class FavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        fav_teachers = UserFavorite.objects.filter(fav_type=3, user=request.user)
        teacher_list = []
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            if Teacher.objects.filter(id=teacher_id):
                teacher = Teacher.objects.get(id=teacher_id)
                teacher_list.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list":teacher_list
        })


class MessageView(LoginRequiredMixin, View):
    def get(self, request):
        mymessages = UserMessage.objects.filter(user=request.user.id)

        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read=True
            unread_message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(mymessages, 3, request=request)

        messages = p.page(page)



        return render(request, "usercenter-message.html", {
            "messages": messages,
        })

