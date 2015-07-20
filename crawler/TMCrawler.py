#-*- coding:utf-8 -*-
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append(r'../')
import re
import json
import random
import time
import base.Common as Common
import base.Config as Config
from Item import Item
from base.RetryCrawler import RetryCrawler
from db.MysqlAccess import MysqlAccess

import warnings
warnings.filterwarnings("ignore")

class TMCrawler():
    '''A class of TMall shop'''
    def __init__(self):
        # 抓取设置
        #self.crawler     = MyCrawler()
        self.crawler     = RetryCrawler()

        # db
        self.mysqlAccess  = MysqlAccess() # mysql access

        # 品牌官网链接
        self.home_url   = 'http://www.taobao.com'
        self.refers     = None

        # 抓取商品列表
        self.link_list  = []
        self.items      = []

        self.begin_time = Common.now()
        
    def getPage(self, url, shop_home_url):
        position = 1
        i = 1
        max_page = 0
       
        asyn_url = ''
        i_url = url
        refers = shop_home_url
        result_s = self.get_asyn_data(i_url, refers, shop_home_url)
        m = re.search(r'<b class="ui-page-s-len">\d+/(\d+)</b>', result_s, flags=re.S) 
        if m:
            max_page = int(m.group(1))
        print '# page num:', max_page
        while i <= max_page:
            m = re.search(r'<div class="J_TItems">(.+?)<div class="pagination">', result_s, flags=re.S)
            if m:
                items_s = m.group(1)
                p = re.compile(r'<dl class=".+?".+?data-id="(.+?)">.+?<dd class="detail">\s*<a class="item-name".+?href="(.+?)".+?>(.+?)</a>\s*<div class="attribute">\s*<div class="cprice-area">\s*<span class="symbol">(.+?)</span>\s*<span\s*class="c-price">(.+?)</span>\s*</div>.+?</dl>')
                j = 1
                for item in p.finditer(items_s):
                    item_id, url_s, item_name, price_symbol, price = item.group(1), item.group(2), Common.htmlDecode(item.group(3).strip()), item.group(4).strip(), item.group(5).strip()
                    if url_s.find('http') == -1:
                        item_url = 'http:' + url_s
                    else:
                        item_url = url_s
                    print '### item ###'
                    print '# item val:', item_id, item_name, price, item_url
                    item = Item()
                    item.parserTM((item_id, item_name, price, item_url, i_url, self.begin_time))
                    print '# item info:',item.outItemSql()
                    self.mysqlAccess.insert_parser_item_info(item.outItemSql())
                    time.sleep(2)
            
            refers = i_url
            if i_url.find('pageNo=') == -1:
                i_url = re.sub(r'&tsearch=y','&pageNo=%d&tsearch=y#anchor' % i, refers)
            else:
                i_url = re.sub(r'&pageNo=\d+&','&pageNo=%d&' % i, refers)

            i += 1
            time.sleep(2)
            result_s = self.get_asyn_data(i_url, refers, shop_home_url)

    def get_asyn_data(self, i_url, refers, shop_home_url):
        result = ''
        result_s = ''
        page = self.crawler.getData(i_url, refers)
        m = re.search(r'<input id="J_ShopAsynSearchURL".+?value="(.+?)"\s*/>', page, flags=re.S)
        if m:
            ts = '?_ksTS=%s&callback=jsonp135&' % (str(int(time.time()*1000)) + '_' + str(random.randint(100,999)))
            a_url = shop_home_url + Common.htmlDecode(m.group(1))
            asyn_url = re.sub('\?', ts, a_url)
            result = self.crawler.getData(asyn_url, i_url)
            m = re.search(r'jsonp135\("(.+?)"\)', result, flags=re.S)
            if m:
                result_s = re.sub(r'\\"', '"', m.group(1))
        return result_s


    def getItems(self):
        #for link in self.link_list: self.itemPage(link)
        max_th = 10
        #if len(self.link_list) > max_th:
        #    m_itemsObj = BagItemM(self.home_url,self.brand_type, max_th)
        #else:
        #    m_itemsObj = BagItemM(self.home_url,self.brand_type, len(self.link_list))
        #m_itemsObj.createthread()
        #m_itemsObj.putItems(self.link_list)
        #m_itemsObj.run()
        #self.items.extend(m_itemsObj.items)

    def itemPage(self, val):
        print '# itemPage :', serie_title, i_title, i_name, i_price, i_unit, i_size, i_url, i_img

if __name__ == '__main__':
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    #home_url = 'http://watsons.tmall.com'
    #url = 'http://watsons.tmall.com/search.htm?search=y&orderType=hotsell_desc&tsearch=y'
    home_url = 'http://mannings.tmall.com'
    url = 'http://mannings.tmall.com/search.htm?scene=taobao_shop&search=y&orderType=hotsell_desc&tsearch=y'
    t = TMCrawler()
    t.getPage(url,home_url)
    #t.getItems()
    
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    
