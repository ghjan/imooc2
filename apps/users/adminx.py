# _*_ coding: utf-8 _*_
# __author__ = 'david'
# __date__ = '2018/5/19 23:34'
#
import xadmin
import xadmin.views as xviews

from .models import EmailVerifyRecord, Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(xviews.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    site_title = "慕雪后台管理系统"
    site_footer = "慕雪在线网"
    menu_style = "accordion"  # 默认每个app收起来


xadmin.site.register(xviews.CommAdminView, GlobalSettings)


class EmailVerifyRecordAdmin(object):
    # 后台列表显示列
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 后台列表查询条件
    search_fields = ['code', 'email', 'send_type']
    # 后台列表通过时间查询
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-user'


class BannerAdmin(object):
    # 后台列表显示列
    list_display = ['index', 'title', 'image', 'url', 'add_time']
    # 后台列表查询条件
    search_fields = ['index', 'title', 'image', 'url']
    # 后台列表通过时间查询
    list_filter = ['index', 'title', 'image', 'url', 'add_time']
    model_icon = 'fa fa-flag'


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
