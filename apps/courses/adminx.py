# _*_ coding: utf-8 _*_
__author__ = 'david'
__date__ = '2018/5/20 10:31'

import xadmin
from .models import Course, Lesson, Video, CourseResource, BannerCourse


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    # 后台列表显示列
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'get_zj_nums', 'go_to', 'fav_num',
                    'click_num',
                    'teacher',
                    'course_org', 'category', 'tag', 'add_time',
                    ]
    # 后台列表查询条件
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_num', 'teacher__name',
                     'click_num',
                     'course_org__name']
    # 后台列表通过时间查询
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_num', 'click_num',
                   'teacher__name', 'add_time',
                   'course_org__name']
    model_icon = 'fa fa-book'
    ordering = ['-click_num']
    readonly_fields = ('click_num',)
    list_editable = ('degree', 'desc')  # 直接在列表页面进行编辑
    exclude = ('fav_num',)
    inlines = [LessonInline, CourseResourceInline]
    style_fields = {"detail": "ueditor"}
    import_excel = True

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 保存课程的时候，课程机构重新统计当前的课程数量
        obj = self.new_obj
        obj.save()
        if obj.course_org:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org)
            course_org.save()

    def post(self, request, *args, **kwargs):
        #  导入逻辑
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    # 后台列表显示列
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_num', 'click_num', 'teacher',
                    'course_org', 'category', 'tag', 'add_time',
                    ]
    # 后台列表查询条件
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_num', 'teacher__name',
                     'click_num',
                     'course_org__name']
    # 后台列表通过时间查询
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_num', 'click_num',
                   'teacher__name', 'add_time',
                   'course_org__name']
    model_icon = 'fa fa-book'
    ordering = ['-click_num']
    readonly_fields = ('click_num',)
    exclude = ('fav_num',)
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    # 后台列表显示列
    list_display = ['course', 'name', 'add_time']
    # 后台列表查询条件
    search_fields = ['course__name', 'name']
    # 后台列表通过时间查询
    list_filter = ['course__name', 'name', 'add_time']
    model_icon = 'fa fa-bars'


class VideoAdmin(object):
    # 后台列表显示列
    list_display = ['lesson', 'name', 'url', 'add_time']
    # 后台列表查询条件
    search_fields = ['lesson__name', 'url', 'name']
    # 后台列表通过时间查询
    list_filter = ['lesson__name', 'name', 'url', 'add_time']
    model_icon = 'fa fa-file-video-o'


class CourseResourceAdmin(object):
    # 后台列表显示列
    list_display = ['course', 'name', 'download', 'add_time']
    # 后台列表查询条件
    search_fields = ['course__name', 'download', 'name']
    # 后台列表通过时间查询
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
