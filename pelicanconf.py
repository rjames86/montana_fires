#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

BASE_BLOG_PATH = os.path.abspath(os.path.join(__file__, os.pardir))

# Set up some path names
CONTENT_PATH = os.path.join(BASE_BLOG_PATH, 'content')

AUTHOR = u'Ryan M'
SITENAME = u'Montana Fires'
SITEURL = 'http://localhost:8000'

PATH = 'content'

OUTPUT_PATH = os.path.join('/', 'tmp', 'montana_fires')

TIMEZONE = 'America/Los_Angeles'
DEFAULT_DATE_FORMAT = '%B %d, %Y at %H:%M:%S %Z'
THEME = 'theme/nice-blog'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'json_reader',
]

# Blogroll
LINKS = ()

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = 10

# THEME = 'themes/pelican-themes/bricabrac'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


# Theme stuff
SIDEBAR_DISPLAY = ['categories']

