# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import time
import pymongo
import settings
from items import FangspiderItem
from datetime import datetime


class FangspiderPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(host=settings.Mongodb_Host,port=settings.Mongodb_Port)
        db = client["fangdb"]
        nowtime = datetime.now().strftime('%Y%m%d%H%M%S')
        self.newfanginfo = db[nowtime]

    def process_item(self,item,spider):
        if isinstance(item,FangspiderItem):
            try:
                self.newfanginfo.insert(dict(item))
            except Exception as e:
                print e
        return item