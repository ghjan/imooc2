# -*- coding: utf-8 -*-

from courses.models import Course
from organization.models import CourseOrg, Teacher

FAV_CLASSES = {1: Course, 2: CourseOrg, 3: Teacher}
FAV_TEMPLATES = {1: 'usercenter_fav_course.html', 2: 'usercenter_fav_org.html', 3: 'usercenter_fav_teacher.html'}


def change_fav_num(fav_id, fav_type, increase=True):
    """
    收藏/取消收藏
    :param fav_id:收藏objectid
    :param fav_type:收藏類型
    :param increase:是否增加收藏
        False:取消收藏
    """
    class_ = FAV_CLASSES.get(int(fav_type))
    obj = class_.objects.get(id=int(fav_id))
    obj.fav_num = (obj.fav_num + 1) if increase else (obj.fav_num - 1)
    if obj.fav_num < 0:
        obj.fav_num = 0
    obj.save()
