#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'charles'
SITENAME = 'checkroth-site'
SITEURL = ''
SITEDESCRIPTION = 'My Blog'
SITETITLE = 'Charles Henry Heckroth'
SITESUBTITLE = 'My Notes & Blog'
# SITELOGO = 'https://avatars3.githubusercontent.com/u/1385951?s=460&v=4'e
SITELOGO = '/images/me.jpg'
FAVICON = ''
BROWSER_COLOR = '#FFFFFF'
THEME = 'Flex'
PATH = 'content'
PYGMENTS_STYLE = 'colorful'

TIMEZONE = 'Japan'


I18N_TEMPLATES_LANG = 'en'
DEFAULT_LANG = 'en'
OG_LOCALE = 'en_US'
LOCALE = 'en_US.UTF-8'

DATE_FORMATS = {
    'en': '%B %d, %Y',
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

USE_FOLDER_AS_CATEGORY = True

# Blogroll
LINKS = (('Blog', '/blog_index.html'),
         ('Resume',
          'https://drive.google.com/file/d/1HLklPEKD8CMGnUfddLsOewxYlIfioJxq/view'),
         ('BeProud', 'https://www.beproud.jp'),
         )


# Social widget
SOCIAL = (('envelope', 'mailto:checkroth@gmail.com'),
          ('github', 'https://www.github.com/Checkroth'),
          ('linkedin', 'https://www.linkedin.com/in/charlesheckroth'),
          ('twitter', 'http://www.twitter.com/checkroth'),
          ('stack-overflow', 'https://stackoverflow.com/users/1037971/charles'),
          )


# Local site links
HOME_HIDE_TAGS = False
INDEX_SAVE_AS = 'blog_index.html'
MAIN_MENU = True
MENUITEMS = (('Blog', '/blog_index.html'),
             ('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

DEFAULT_PAGINATION = 10

CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike',
    'version': '4.0',
    'slug': 'by-sa'
}
COPYRIGHT_YEAR = 2019


STATIC_PATHS = ['extra', 'images']
EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'static/custom.css'},
    'extra/CNAME': {'path': 'CNAME'},
}
CUSTOM_CSS = 'static/custom.css'

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# External Service Mixins
GOOGLE_ANALYTICS = 'UA-136401999-1'
DISQUS_SITENAME = 'checkroth'
GOOGLE_ADSENSE = {
    'ca_id': 'ca-pub-3090577057275093',
    'page_level_ads': True,
    'ads': {
    }
}
