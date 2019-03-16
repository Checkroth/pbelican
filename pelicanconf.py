#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'charles'
SITENAME = 'checkroth-site'
SITEURL = ''
SITEDESCRIPTION = 'My Blog'
SITELOGO = ''
FAVICON = ''
BROWSER_COLOR = '#FFFFFF'
THEME = 'Flex'
PATH = 'content'
PYGMENTS_STYLE = 'colorful'

TIMEZONE = 'Japan'


I18N_TEMPLATES_LANG = 'en'
DEFAULT_LANG = 'en'
OG_LOCALE = 'en_US'
LOCALE = 'en_US'

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
LINKS = (('Resume',
          'https://drive.google.com/file/d/0B2kTdZ0fBWzhaHBUOFlzYjNrRjg/view?usp=sharing'),
         ('BeProud', 'https://beproud.jp'),
         )


# Social widget
SOCIAL = (('github', 'https://www.github.com/Checkroth'),
          ('linkedin', 'https://www.linkedin.com/in/charlesheckroth'),
          ('twitter', 'http://www.twitter.com/checkroth'),
          )


# Local site links
MAIN_MENU = True
MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
