#-*- coding:utf-8 -*-
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append(r'../')
import re
import json
import time
import base.Common as Common
import base.Config as Config
from base.RetryCrawler import RetryCrawler
from db.MysqlAccess import MysqlAccess

import warnings
warnings.filterwarnings("ignore")

class taobaoSearch():
    '''A class of taobao search page'''
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
        self.brand_names = ["艾沃","保宁","红太阳","常润","厨邦","大华","大同","大王","德馨斋","德阳","东古","凤球唛","福临门","高真","古龙","冠生园","广味源","广祥泰","龟甲万","国味威","海鸥","海天","好伴","禾然","和田宽","恒顺","湖西岛","湖羊","黄花园","南食召","吉成","济美","加加","金冠园","金兰","金狮","有味家","金苏","荆楚","景山","居易","聚百鲜","科沁万佳","孔膳坊","快鹿","阆中","老才臣","食味的初相","老蔡","老恒和","老潘头","李锦记","利民","六月鲜","春峰","龙菲","秋生饭堂","龙牌","隆昌","楼茂记","鲁花自然鲜","云上","禄荣","麻旺","美富达","美极","美味源","蒙古真","渔山隐","米吉真味","酿一村","盘溪","彭万春","浦源","奇峰","千禾","千鹤屋","粮赞","钱万隆","清净园","清香园","仁昌记","三不加","悦意","三和四美","博爱酵园","山古坊","膳府","膳之堂","盛田","四海","寺冈","苏美","太太乐","泰康","唐人基","唐世家","淘大","腾安","同珍","妥甸","拓东","丸天","万通","万字","味事达","五天","犀浦","仙家","先市","鲜渡","咸亨","香满园","小东字","笑厨","新宇","星湖","徐同泰","薛泰丰","扬名","尧记","肴易食","一统原创","一休屋","伊例家","宜赤必","优和","鱼味鲜","禹谟","玉堂","御酿坊","缘木记","粤香园","灶基","詹王","张家三嫂","长寿结","珍极","正信","正阳河","至味","致美斋","中邦","中冷泉","中调","珠江桥","梓山","自然集","佐参王","佐香园","中坝","天府","南吉","清湖","味华","佐餐王","一品江南","金顶","玉河","巧媳妇","齐鲁","梁山好汉","王家园子","食圣","山口","川鹰","德通","新汶","四海","德馨斋","玉兔","灯塔","仙鹤","宏林","贵族王中王","万和","口珍","同福永","威极","嘉美乐","天浩圆","铁鸟","恒裕","周太","海鸥","太阳岛","百花","小神厨","龙菲","太和","天一","美乐","三汇","通海","黑珍珠","百乐","吉鹤村","岭桥","瓦缸","味莼园","百花串","锦酿","福香居","铁石","石桥","清华","味邦","光华","罕王","营宝","非常","大有丰","沙陀","味味晓","云晓","巧妈妈","振龙","乾缘","稻香园","一品斋","孔雀","武大郎","绿芳","天赐","益彰","建洛","天口","一品江南","机轮","溢美堂","山乡","榕江","嘉乐美","万路通","肖大妈","争荣","仙源","敬义泰","昆湖","鼎兴","临江寺","迈进","玉和","通德","民天","胡玉美","楼茂记","鼎丰","古灯","槐茂","榕城","BB","汉记","松城","森江","美狮","龙华","启航","隆邦","新汶","四海","龙之味","北康","金玉兰","小二黑","吉成"]
        
    def getPage(self, url):
        position = 1
        i = 1
       
        i_url = url
        refers = self.home_url
        max_page = 10
        size_page = 48
        while i <= max_page:
            page = self.crawler.getData(i_url, refers)
            refers = i_url
            i_url = url + '&bcoffset=1&s=%s' % str(i*size_page)
            i += 1
            if not page or page == '':
                print 'not find data url:',i_url
                time.sleep(4)
                continue
            m = re.search(r'<script>\s+g_page_config = ({.+?});.+?</script>', page, flags=re.S)
            if m:
                page_config = m.group(1)
                page_config_s = re.sub(r'\n+','',page_config)
                data = json.loads(page_config_s)
                if data.has_key("mods"):
                    if data["mods"].has_key("itemlist"):
                        itemlist = data["mods"]["itemlist"]
                        if itemlist.has_key("data"):
                            itemlist_data = itemlist["data"]
                            if itemlist_data.has_key("auctions"):
                                for item in itemlist_data["auctions"]:
                                    item_id = position
                                    m = re.search(r'id=(\d+)', item["detail_url"], flags=re.S)
                                    if m:
                                        item_id = m.group(1)
                                    item_sales = item["view_sales"]
                                    m = re.search(r'(\d+)', item["view_sales"], flags=re.S)
                                    if m:
                                        item_sales = m.group(1)
                                    print Common.time_s(Common.now()), position, item_id, item["raw_title"], item["view_price"], item_sales, item["user_id"], item["nick"], "http:" + item["detail_url"], "http:" + item["shopLink"]
                                    self.mysqlAccess.insert_item((Common.time_s(Common.now()), str(item_id), str(position), str(item["raw_title"]), str(item["view_price"]), str(item_sales), "http:" + item["detail_url"], item["user_id"], str(item["nick"]), "http:" + item["shopLink"]))
                                    position += 1
            time.sleep(4)


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

    def outItems(self, f):
        s = '#系列名称|商品标签|商品名称|商品价格|金额单位|商品尺寸|商品链接|商品图片|商品编号'
        with open(f, 'w') as f_item:
            self.items.insert(0, s)
            f_item.write('\n'.join(self.items))

if __name__ == '__main__':
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    t = taobaoSearch()
    #url = 'http://s.taobao.com/search?q=%E9%85%B1%E6%B2%B9&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20150702&ie=utf8&sort=sale-desc'
    url = 'http://s.taobao.com/search?q=%E5%B7%B4%E6%8B%BF%E7%B1%B3&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20150702&ie=utf8&sort=sale-desc'
    t.getPage(url)
    #t.getItems()
    
    #f = Config.dataPath + 'dior_%s.txt' %Common.today_ss()
    #b.outItems(f)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    
