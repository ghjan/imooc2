#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @desc:
 @author: david
 @date: 2018/11/19 0019
"""

# coding:utf-8

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


# excel 导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    # 返回True的时候，加载本插件
    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string(
            'xadmin/excel/model_list.top_toolbar.import.html', context=context.dicts[1]
        ))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)
