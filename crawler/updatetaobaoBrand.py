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
from db.MysqlAccess import MysqlAccess

import warnings
warnings.filterwarnings("ignore")

class updatetaobaoBrand():
    '''A class of update taobao Brand'''
    def __init__(self):
        # db
        self.mysqlAccess  = MysqlAccess() # mysql access

        self.brand_names = ["艾沃","保宁","红太阳","常润","厨邦","大华","大同","大王","德馨斋","德阳","东古","凤球唛","福临门","高真","古龙","冠生园","广味源","广祥泰","龟甲万","国味威","海鸥","海天","好伴","禾然","和田宽","恒顺","湖西岛","湖羊","黄花园","南食召","吉成","济美","加加","金冠园","金兰","金狮","有味家","金苏","荆楚","景山","居易","聚百鲜","科沁万佳","孔膳坊","快鹿","阆中","老才臣","食味的初相","老蔡","老恒和","老潘头","李锦记","利民","六月鲜","春峰","龙菲","秋生饭堂","龙牌","隆昌","楼茂记","鲁花自然鲜","云上","禄荣","麻旺","美富达","美极","美味源","蒙古真","渔山隐","米吉真味","酿一村","盘溪","彭万春","浦源","奇峰","千禾","千鹤屋","粮赞","钱万隆","清净园","清香园","仁昌记","三不加","悦意","三和四美","博爱酵园","山古坊","膳府","膳之堂","盛田","四海","寺冈","苏美","太太乐","泰康","唐人基","唐世家","淘大","腾安","同珍","妥甸","拓东","丸天","万通","万字","味事达","五天","犀浦","仙家","先市","鲜渡","咸亨","香满园","小东字","笑厨","新宇","星湖","徐同泰","薛泰丰","扬名","尧记","肴易食","一统原创","一休屋","伊例家","宜赤必","优和","鱼味鲜","禹谟","玉堂","御酿坊","缘木记","粤香园","灶基","詹王","张家三嫂","长寿结","珍极","正信","正阳河","至味","致美斋","中邦","中冷泉","中调","珠江桥","梓山","自然集","佐参王","佐香园","中坝","天府","南吉","清湖","味华","佐餐王","一品江南","金顶","玉河","巧媳妇","齐鲁","梁山好汉","王家园子","食圣","山口","川鹰","德通","新汶","四海","德馨斋","玉兔","灯塔","仙鹤","宏林","贵族王中王","万和","口珍","同福永","威极","嘉美乐","天浩圆","铁鸟","恒裕","周太","海鸥","太阳岛","百花","小神厨","龙菲","太和","天一","美乐","三汇","通海","黑珍珠","百乐","吉鹤村","岭桥","瓦缸","味莼园","百花串","锦酿","福香居","铁石","石桥","清华","味邦","光华","罕王","营宝","非常","大有丰","沙陀","味味晓","云晓","巧妈妈","振龙","乾缘","稻香园","一品斋","孔雀","武大郎","绿芳","天赐","益彰","建洛","天口","一品江南","机轮","溢美堂","山乡","榕江","嘉乐美","万路通","肖大妈","争荣","仙源","敬义泰","昆湖","鼎兴","临江寺","迈进","玉和","通德","民天","胡玉美","楼茂记","鼎丰","古灯","槐茂","榕城","BB","汉记","松城","森江","美狮","龙华","启航","隆邦","新汶","四海","龙之味","北康","金玉兰","小二黑","吉成"]

    def update_item_brand(self):
        items = self.mysqlAccess.get_allitems()
        for item in items:
            brandnames = ''
            item_id, item_name = item
            for brandname in self.brand_names:
                if item_name.find(brandname) != -1:
                    brandnames += brandname + '|'
            if brandnames != '':
                print item_id, item_name, brandnames[:-1]
                self.mysqlAccess.update_item_brand((brandnames[:-1],str(item_id)))

if __name__ == '__main__':
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    t = updatetaobaoBrand()
    t.update_item_brand()
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    
