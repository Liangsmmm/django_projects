# _*_ encoding: utf-8 _*_
import xadmin

from course.models import Course,CourseResource,Lesson,Video


class CourseAdmin(object):
    list_display=['name','desc','detail','degree','learn_times','students','fav_nums']
    search_fields=['name','desc','detail','degree','learn_times','students','fav_nums']
    list_filter=['name','desc','detail','degree','learn_times','students','fav_nums']
    # ordering = ['-click_nums']
    # readonly_fields = ['click_nums']
    # list_editable = ['degree', 'desc']
    # exclude = ['fav_nums']
    # inlines = [LessonInline, ]
    style_fields = {"detail":"ueditor"}
    import_excel = True

    # def queryset

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, *args, **kwargs)


class CourseResourceAdmin(object):
    list_display=['course','name','add_time']
    search_fields=['course','name']
    list_filter=['course','name']


class LessonAdmin(object):
    list_display=['course','name','add_time']
    search_fields=['course','name']
    list_filter=['course','name']


class VideoAdmin(object):
    list_display=['lesson','name','add_time']
    search_fields=['lesson','name']
    list_filter=['lesson','name']


xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)

