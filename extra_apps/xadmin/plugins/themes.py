# coding:utf-8
from __future__ import print_function
import os
import httplib2
import requests
from django.template import loader
from django.core.cache import cache
from django.utils import six
from django.utils.translation import ugettext as _
from xadmin.sites import site
from xadmin.models import UserSettings
from xadmin.views import BaseAdminPlugin, BaseAdminView
from xadmin.util import static, json
import six

if six.PY2:
    import urllib
else:
    import urllib.parse

THEME_CACHE_KEY = 'xadmin_themes'


class ThemePlugin(BaseAdminPlugin):
    enable_themes = False
    # {'name': 'Blank Theme', 'description': '...', 'css': 'http://...', 'thumbnail': '...'}
    user_themes = None
    use_bootswatch = False
    default_theme = static('xadmin/css/themes/bootstrap-xadmin.css')
    bootstrap2_theme = static('xadmin/css/themes/bootstrap-theme.css')

    def init_request(self, *args, **kwargs):
        return self.enable_themes

    def _get_theme(self):
        if self.user:
            try:
                return UserSettings.objects.get(user=self.user, key="site-theme").value
            except Exception:
                pass
        if '_theme' in self.request.COOKIES:
            if six.PY2:
                func = urllib.unquote
            else:
                func = urllib.parse.unquote
            return func(self.request.COOKIES['_theme'])
        return self.default_theme

    def get_context(self, context):
        context['site_theme'] = self._get_theme()
        return context

    # Media
    def get_media(self, media):
        return media + self.vendor('jquery-ui-effect.js', 'xadmin.plugin.themes.js')

    # Block Views
    def block_top_navmenu(self, context, nodes):

        themes = [
            {'name': _(u"Default"), 'description': _(u"Default bootstrap theme"), 'css': self.default_theme},
            {'name': _(u"Bootstrap2"), 'description': _(u"Bootstrap 2.x theme"), 'css': self.bootstrap2_theme},
        ]
        select_css = context.get('site_theme', self.default_theme)

        if self.user_themes:
            themes.extend(self.user_themes)

        if self.use_bootswatch:
            ex_themes = cache.get(THEME_CACHE_KEY)
            if ex_themes:
                themes.extend(json.loads(ex_themes))
            else:
                ex_themes = []
                flag = False  # 假如为True使用原来的代码，假如为Flase，使用requests库来访问
                url_bootswath = "https://bootswatch.com/api/3.json"
                header1 = {"Accept": "application/json",
                           "User-Agent": self.request.META['HTTP_USER_AGENT']}
                headers2 = {
                    'content-type': 'application/json',
                    "accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
                    "accept-encoding": "gzip, deflate, br",
                    "User-Agent":
                        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
                    "upgrade-insecure-requests": "1",

                }
                ck = "__cfduid=d13ae6de34090a59037f21e453bbc267a1526834776; cf_clearance=10fff22cb373a1c8b10204b489658f34b0c9ad8d-1526834783-3600; __utma=97413516.806424570.1526835277.1526835277.1526835277.1; __utmc=97413516; __utmz=97413516.1526835277.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmb=97413516.2.10.1526835277"
                cookies = {}
                for line in ck.split(';'):
                    name, value = line.strip().split('=', 1)
                    cookies[name] = value  # 为字典cookies添加内容

                watch_themes = []
                try:
                    if flag:
                        h = httplib2.Http()
                        resp, content = h.request(url_bootswath, 'GET', '',
                                                  headers=headers2)
                        if six.PY3:
                            content = content.decode()
                        watch_themes = json.loads(content)['themes']
                    else:
                        session = requests.Session()

                        content = session.get(url_bootswath, cookies=cookies, headers=headers2, verify=False)
                        if six.PY3:
                            if not isinstance(content.text, str):
                                content = content.text.decode()
                        watch_themes = json.loads(content.text)['themes']

                except Exception as e:
                    jsonFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'themes3.json')
                    with open(jsonFile, 'r') as f:
                        watch_themes = json.loads(f.read())['themes']
                ex_themes.extend([
                    {'name': t['name'], 'description': t['description'],
                     'css': t['cssMin'], 'thumbnail': t['thumbnail']}
                    for t in watch_themes])

                cache.set(THEME_CACHE_KEY, json.dumps(ex_themes), 24 * 3600)
                themes.extend(ex_themes)

        nodes.append(
            loader.render_to_string('xadmin/blocks/comm.top.theme.html', {'themes': themes, 'select_css': select_css}))


site.register_plugin(ThemePlugin, BaseAdminView)
