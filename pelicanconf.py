#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'charles'
SITENAME = 'software-and-stuff'
SITEURL = 'https://checkroth.com'
SITEURL = ''
SITEDESCRIPTION = 'Blog and info'
SITETITLE = 'Charles Henry Heckroth'
SITESUBTITLE = 'My Notes & Blog'
SITELOGO = '/images/me.jpg'
FAVICON = ''
BROWSER_COLOR = '#FFFFFF'
THEME = 'Flex'
PATH = 'content'
PYGMENTS_STYLE = 'colorful'

TIMEZONE = 'Japan'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['pelican-toc']


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
LINKS = (
    ('Blog', '/'),
    ('Resume', 'https://drive.google.com/file/d/1HLklPEKD8CMGnUfddLsOewxYlIfioJxq/view'),
)

# Social widget
SOCIAL = (('envelope', 'mailto:checkroth@gmail.com'),
          ('github', 'https://www.github.com/Checkroth'),
          ('linkedin', 'https://www.linkedin.com/in/charlesheckroth'),
          ('twitter', 'http://www.twitter.com/checkroth'),
          ('stack-overflow', 'https://stackoverflow.com/users/1037971/charles'),
          )
TWITTER_USERNAME = '@checkroth'


# Local site links
HOME_HIDE_TAGS = False
MAIN_MENU = True
MENUITEMS = (('Blog', '/'),
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
        'aside': '7734708573',
        'article_bottom': '6895080254',
    }
}

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {},
    },
    'output_format': 'html5',
}


TOC = {
    'TOC_HEADERS'       : '^h[1-6]', # What headers should be included in
                                     # the generated toc
                                     # Expected format is a regular expression

    'TOC_RUN'           : 'true',    # Default value for toc generation,
                                     # if it does not evaluate
                                     # to 'true' no toc will be generated

    'TOC_INCLUDE_TITLE': 'true',     # If 'true' include title in toc
}
