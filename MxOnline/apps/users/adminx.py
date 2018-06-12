# _*_ encoding: utf-8 _*_
import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row

from .models import EmailVerifyRecord, Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = u"慕学后台管理系统"
    site_footer = u"慕学在线网"
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display=['email','code','send_type','send_time']
    search_fields=['email','code','send_type','send_time']
    list_filter=['email','code','send_type','send_time']


class BannerAdmin(object):
    list_display=['title','index','add_time']
    search_fields=['title','index']
    list_filter=['title','index']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
