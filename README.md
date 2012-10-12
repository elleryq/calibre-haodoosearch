calibre-haodoosearch
====================

## 好讀搜索支援

替 Calibre 增加好讀的商店支援，透過這個插件就可以直接搜索好讀網站並下載。

Calibre 是知名的電子書管理軟體，支援各種作業系統，包括 Windows, MacOS
X, Linux 等。網頁：http://calibre-ebook.com/

## 安裝


從 http://github.com/elleryq/calibre-haodoosearch/zipball/master 下載以後，
請先解開到資料夾，然後選取資料夾裡的檔案之後，再壓縮為 zip。就是 zip 檔案裡
不能有資料夾 (github 提供下載的 zip 會有資料夾)。然後從 Calibre 的偏好設定
中安裝。

## 使用說明

啟動 Calibre 以後，可以點選上方的「取得書籍」，即可在左邊找到 Haodoo，
勾選以後，就可以在上方輸入關鍵字進行搜索，搜索後並可以下載。

## 使用的雲端服務

在 0.1 版使用了 Google custom search 來作為資料來源，但是發現這樣的效果並不好。
主要是因為好讀網站上的一頁裡可能有多本書，在 Calibre 裡並不好處理。因此有必要
自行打造網路爬蟲，在一個巧合下知道了有 scraperwiki 這個雲端服務，試用以後，就
決定改用這個來當作資料來源。這部份的代碼也是公開的，請參考下列連結：

 * 爬蟲：https://scraperwiki.com/scrapers/haodooscraper/
 * 資料產出：https://scraperwiki.com/views/haodooscraperview/

## HaoDoo PDB Calibre Plugin

Add HaoDoo store support to Calibre Stores.

Calibre is a populer E-book management program, available for various
platform include Windows, MacOS X, Linux. Link: http://calibre-ebook.com/

## Install

Add the entire project to a zip file or download from
http://github.com/elleryq/calibre-haodoosearch/zipball/master then install
from Calibre preference page.

## Usage

After launching Calibre, you can click "Get books" to open store UI.
You can check "Haodoo" in left column then enter keyword to search/download.

## Cloud service
In first version, I use Google custom search as the data source.  But I found
a page could contain multiple books in Haodoo web site.  I cannot handle this
case in Calibre.
Some day I know there is a cloud service: scraperwiki.  I can use this service
to build my scraper and use it as data source.  The code is opened in 
scraperwiki.com:

 * Scraper：https://scraperwiki.com/scrapers/haodooscraper/
 * Data view：https://scraperwiki.com/views/haodooscraperview/

