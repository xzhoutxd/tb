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
from base.RetryCrawler import RetryCrawler
#from base.TBCrawler import TBCrawler

class Item():
    '''A class of item'''
    def __init__(self):
        # crawler
        #self.crawler         = TBCrawler()
        self.crawler         = RetryCrawler()

        # shop
        self.shop_type       = '1' # 店铺类型
        self.seller_id       = ''   # 卖家ID
        self.seller_name     = ''   # 卖家Name
        self.shop_id         = ''   # 店铺ID
        self.shop_name       = ''   # 店铺Name
        self.shop_url        = ''   # 店铺URL

        # refers
        self.refers          = ''

        # 成交抓取参数
        self.deal_pageSize   = 15
        self.deal_maxPages   = 100
        self.deal_bufferdays = 3   # 往前追溯3天

        # 评价抓取参数
        self.rate_pageSize   = 20
        self.rate_maxPages   = 100

        # 初始化实例变量
        self.initItem()

    def initItem(self):
        # 商品抓取设置
        self.crawling_time   = Common.now()
        self.crawling_begintime = '' # 本次抓取开始时间
        self.crawling_beginDate = '' # 本次爬取日期
        self.crawling_beginHour = '' # 本次爬取小时

        # 商品属性
        self.item_id         = ''   # 商品ID
        self.item_name       = ''   # 商品名称
        self.item_price      = ''   # 商品价格
        self.item_url        = ''   # 商品链接
        self.item_spuId      = ''   # SPU ID
        self.item_sellCount  = 0    # 月销售数

        self.brand_name      = ''
        self.brand_id        = ''
        self.category_id     = ''

        # 商品页
        self.item_page       = None # 商品首页

        # item html urls
        self.item_urls       = []   # 商品链接列表

        # item html pages
        #self.item_pages      = []   # 商品网页列表
        self.item_pages      = {}   # 商品网页列表

        # 成交记录
        self.deal_url        = ''
        self.deal_stopCrawl  = False
        self.deal_deadLine   = 0.0  # 上次抓取的成交记录最晚时间
        self.deal_deadLine2  = 0.0  # 本次抓取的成交记录最早时间

    def TMItem(self):
        if self.item_url != '':
            page = self.crawler.getData(self.item_url, self.refers)
            if not page or page == '':
                raise Common.InvalidPageException("# TMItem: not find item page,itemid:%s,item_url:%s"%(str(self.item_id), self.item_url))

            m = re.search(r'sellerId:"(\d+)",', page, flags=re.S)
            if m:
                self.seller_id = m.group(1)
            m = re.search(r'shopId:"(\d+)",', page, flags=re.S)
            if m:
                self.shop_id = m.group(1)
            m = re.search(r'<div class="slogo">\s*<a class="slogo-shopname" href="(.+?)".+?><strong>(.+?)</strong></a>', page, flags=re.S)
            if m:
                self.shop_url, self.shop_name = Common.fix_url(m.group(1)), m.group(2).strip()

            m = re.search(r'TShop\.Setup\((.+?)\);', page, flags=re.S)
            if m:
                TShop_s = m.group(1).strip()
                m = re.search(r'"brand":"(.+?)",', TShop_s, flags=re.S)
                if m:
                    self.brand_name = Common.htmlDecode(m.group(1).strip())
                m = re.search(r'"brandId":"(\d+)",', TShop_s, flags=re.S)
                if m:
                    self.brand_id = m.group(1)
                m = re.search(r'"categoryId":"(\d+)",', TShop_s, flags=re.S)
                if m:
                    self.category_id = m.group(1)
                m = re.search(r'"sellerNickName":"(.+?)",', TShop_s, flags=re.S)
                if m:
                    self.seller_name = Common.urlDecode(m.group(1).strip())

                m = re.search(r'"initApi":"(.+?)",', TShop_s, flags=re.S)
                if m:
                    ts = "&callback=setMdskip&timestamp=%s" % str(int(time.time()*1000))
                    initapi_url = Common.fix_url(m.group(1).strip()) + ts + "&ref=%s" % Common.urlCode(self.refers)
                    init_page = self.crawler.getData(initapi_url, self.item_url)
                    if not init_page and init_page == '':
                        print '# init page is null..'
                    else:
                        m = re.search(r'"sellCountDO":{"sellCount":(\d+),', init_page, flags=re.S)
                        if m:
                            self.item_sellCount = m.group(1)

    def parserTM(self, val):
        self.item_id, self.item_name, self.item_price, self.item_url, self.refers, self.crawling_begintime = val
        # 本次抓取开始日期
        self.crawling_beginDate = time.strftime("%Y-%m-%d", time.localtime(self.crawling_begintime))
        # 本次抓取开始小时
        self.crawling_beginHour = time.strftime("%H", time.localtime(self.crawling_begintime))
        self.TMItem()

    # 输出抓取的网页sql
    def outItemSql(self):
        return (Common.time_s(self.crawling_time),self.item_id,self.item_name,self.item_price,self.item_sellCount,self.item_url,self.seller_id,self.seller_name,self.shop_id,self.shop_name,self.shop_url,self.brand_id,self.brand_name,self.category_id,self.crawling_beginDate,self.crawling_beginHour)
