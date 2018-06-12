# _*_ encoding: utf-8 _*_
import xadmin
#
from operation.models import UserAsk, UserMessage, UserFavorite, UserCourse, CourseComment


class UserAskAdmin(object):
    list_display=['name','mobile','course_name']
    search_fields=['name','mobile','course_name']
    list_filter=['name','mobile','course_name']


class UserMessageAdmin(object):
    # list_display=['user__name','message','has_read','add_time']
    # search_fields=['user__name','message','has_read']
    # list_filter=['user__name','message','has_read']
    list_display=['message','has_read','add_time']
    search_fields=['message','has_read']
    list_filter=['message','has_read']


class UserFavoriteAdmin(object):
    # list_display=['user__username','fav_id','fav_type','add_time']
    # search_fields=['user__username','fav_id','fav_type']
    # list_filter=['user__username','fav_id','fav_type']
    list_display=['fav_id','fav_type','add_time']
    search_fields=['fav_id','fav_type']
    list_filter=['fav_id','fav_type']


class UserCourseAdmin(object):
    # list_display=['user__username','course__name','message']
    # search_fields=['user__username','course__name','message']
    # list_filter=['user__username','course__name','message']
    list_display=['message']
    search_fields=['message']
    list_filter=['message']


class CourseCommentAdmin(object):
    # list_display=['user__username','course__name','comments','add_time']
    # search_fields=['user__username','course__name','comments']
    # list_filter=['user__username','course__name','comments']
    list_display=['comments','add_time']
    search_fields=['comments']
    list_filter=['comments']


xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(CourseComment,CourseCommentAdmin)
