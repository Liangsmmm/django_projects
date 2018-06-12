from django.conf.urls import url, include
from django.views.generic import TemplateView

from .views import CourseListView, CourseDetailView, CourseVideoView, CourseCommentView, AddCommentView




urlpatterns = [

    url(r'^list/$', CourseListView.as_view(), name="course_list"),

    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name="course_video"),
    url(r'^course_comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),
    url(r'^add_comment/$', AddCommentView.as_view(), name="add_comment"),
]
