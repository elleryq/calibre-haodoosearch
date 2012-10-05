# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__ = 'GPL 3'
__copyright__ = '2012, Yan-ren Tsai <elleryq@gmail.com>'
__docformat__ = 'restructuredtext en'

from PyQt4.Qt import QUrl

from calibre.customize import StoreBase
from calibre import browser, url_slash_cleaner
from calibre.gui2 import open_url
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.web_store_dialog import WebStoreDialog
from contextlib import closing
from urllib import urlencode
from lxml import html

try:
    import json
except ImportError:
    print("Cannot import json module.")
    json = None

class HaodooStore(StorePlugin):
    def open(self, parent=None, detail_item=None, external=False):
        print("open")
        url = 'http://www.haodoo.net'

        if external or self.config.get('open_external', False):
            open_url(QUrl(url_slash_cleaner(detail_item if detail_item else url)))
        else:
            d = WebStoreDialog(self.gui, url, parent, detail_item)
            d.setWindowTitle(self.name)
            d.set_tags(self.config.get('tags', ''))
            d.exec_()
        
    def search(self, query, max_results=10, timeout=60):
        print( "search!")
        q = query.decode('utf-8')

        url = "https://views.scraperwiki.com/run/haodooscraperview/?" + urlencode(
                {
                    "q": q
                } )
        #url = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?" + urlencode(
        #        {
        #            "format": "jsondict",
        #            "name": "haodooscraper",
        #            "query": "select * from `bookpages` where title like '%{0}%' or volumes like '%{0}%' limit 10".format( q ),
        #        } )
        print( url )

        br = browser()
        with closing(br.open(url, timeout=timeout)) as f:
            json_doc = f.read()
            if len(json_doc)>0:
                result = json.loads( json_doc )
                for book in result:
                    if not book.has_key('volumes') or not book['volumes']:
                        print( "No volumes, skip." )
                        continue
                    volumes = json.loads( book['volumes'] )
                    print( type( volumes ) )
                    for volume in volumes:
                        s = SearchResult()
                        s.title = volume['title']
                        s.detail_item = book['url']
                        s.price = '$0.00'
                        s.drm = SearchResult.DRM_UNLOCKED

                        if volume.has_key('type') and len(volume["type"]):
                            exts = json.loads( volume["type"] )
                            for t in exts:
                                ext, dl_link = t
                                s.downloads[ext] = dl_link
                            s.formats = ', '.join(s.downloads.keys())
                        yield s

