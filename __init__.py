# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__ = 'GPL 3'
__copyright__ = '2012, Yan-ren Tsai <elleryq@gmail.com>'
__docformat__ = 'restructuredtext en'

from calibre.customize import StoreBase

class HaodooStorePlugin(StoreBase):
    name = 'Haodoo Search Plugin'
    description = _('Search in Haodoo (http://www.haodoo.net)')
    supported_platforms     = ['windows', 'linux']
    author                  = 'Yan-ren Tsai <elleryq@gmail.com>'
    version                 = (0, 3, 0)
    minimum_calibre_version = (0, 8, 0)

    actual_plugin = 'calibre_plugins.store_haodoosearchplugin.haodoo:HaodooStore'

