# _*_ encoding: utf-8 _*_
import xadmin
#
from organization.models import CityDict,CourseOrg,Teacher


class CityDictAdmin(object):
    list_display=['name','desc','add_time']
    search_fields=['name','desc']
    list_filter=['name','desc']


class CourseOrgAdmin(object):
    list_display=['name','desc','click_nums','fav_nums','address','add_time']
    search_fields=['name','desc','click_nums','fav_nums','address']
    list_filter=['name','desc','click_nums','fav_nums','address']
    # list_display=['name','desc','click_nums','fav_nums','address','city__name','add_time']
    # search_fields=['name','desc','click_nums','fav_nums','address','city__name']
    # list_filter=['name','desc','click_nums','fav_nums','address','city__name']


class TeacherAdmin(object):
    list_display=['name','org','work_years','work_company','work_position','points','click_nums','fav_nums']
    search_fields=['name','org','work_years','work_company','work_position','points','click_nums','fav_nums']
    list_filter=['name','org','work_years','work_company','work_position','points','click_nums','fav_nums']


xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)

