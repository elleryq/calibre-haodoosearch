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
        # if json is None:
        #     return None
        key = 'AIzaSyBRSleYvSyG-Bxo9_6-4TJalmkw77jMzmo'
        cx = '015871176235127732549:or0582yikva'
        q = query.decode('utf-8')
        
        # default is unicode string, so we encode as utf-8 after string is formated.
        url = "https://www.googleapis.com/customsearch/v1?" + urlencode( {
            "key": key,
            "cx": cx,
            "q": q
            } )
        print( url )

        br = browser()

        with closing(br.open(url, timeout=timeout)) as f:
            json_doc = f.read()
            results = json.loads( json_doc )
            for data in results['items']:
                s = SearchResult()
                s.title = data["title"].strip()
                s.detail_item = data["link"].strip()
                s.price = '$0.00'
                s.drm = SearchResult.DRM_UNLOCKED

                yield s

    def get_details(self, search_result, timeout):
        print("get_details")
        try:
            print( search_result.detail_item )
        except:
            pass

        url = url_slash_cleaner( search_result.detail_item )
        br = browser()
        with closing(br.open(url, timeout=timeout*2)) as nf:
            content = nf.read()
            doc = html.fromstring(content)

            for save_item in doc.xpath('//input[contains(@type, "button")]'):
                onclick = save_item.get('onclick')
                if "DownloadEpub" in onclick:
                    self.__handle( search_result, onclick, "epub" )
                elif "DownloadUpdb" in onclick:
                    self.__handle( search_result, onclick, "updb" )
                elif "DownloadPdb" in onclick:
                    self.__handle( search_result, onclick, "pdb" )

        return True

    def __find_book_id( self, onclick ):
        # find which kind of quote, ' or "
        quote = "'"
        try:
            start = onclick.index( quote )
        except ValueError: 
            quote = '"'

        book_id = ''
        try:
            start = onclick.index( quote )
            end = onclick.rindex( quote )
            book_id = onclick[ start+1:end ]
        except:
            pass

        return book_id

    def __convert_to_dl_url( self, book_id, ext ):
        result = "http://www.haodoo.net/?" + urlencode( {
            "M": "d",
            "P": book_id+"." + ext } )
        #print( "__convert_to_dl_url()=%s" % result )
        return result

    def __handle( self, search_result, onclick, book_type ):
        # retrieve only the parameter in javascript.
        book_id = self.__find_book_id( onclick )
        if not book_id:
            print( "Cannot extract book_id" )
            return

        # convert to download link
        dl_link = self.__convert_to_dl_url( book_id, book_type )

        # put in search result.
        search_result.downloads[book_type] = dl_link
        search_result.formats = ', '.join(search_result.downloads.keys())

