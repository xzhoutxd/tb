#-*- coding:utf-8 -*-
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append(r'../')
import base.Common as Common
import traceback
import MysqlPool

class MysqlAccess():
    '''A class of mysql db access'''
    def __init__(self):
        self.db = MysqlPool.tb_DbPool

    def __del__(self):
        self.db = None

    def insert_parser_item_info(self, args):
        try:
            sql = 'replace into nd_tb_parser_item_info(crawl_time,item_id,item_name,item_price,item_sale,item_url,seller_id,seller_name,shop_id,shop_name,shop_url,brand_id,brand_name,category_id,c_begindate,c_beginhour) values(%s)' % Common.aggregate(16)
            self.db.execute(sql, args)
        except Exception, e:
            print '# insert tb shop item exception:', e

    def insert_item(self, args):
        try:
            sql = 'replace into nd_tb_parser_item(crawl_time,item_id,position,item_name,item_price,item_sale,item_url,seller_id,seller_name,shop_url) values(%s)' % Common.aggregate(10)
            self.db.execute(sql, args)
        except Exception, e:
            print '# insert tb item exception:', e

    def get_allitems(self):
        try:
            sql = 'select item_id,item_name from nd_tb_parser_item'
            return self.db.select(sql)
        except Exception, e:
            print '# select items exception:', e

    def update_item_brand(self, args):
        try:
            sql = 'update nd_tb_parser_item set brand_name = %s where item_id = %s'
            self.db.execute(sql, args)
        except Exception, e:
            print '# update items brand names exception:', e


if __name__ == '__main__':
    my = MysqlAccess()
