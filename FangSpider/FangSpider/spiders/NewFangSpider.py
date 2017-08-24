# -*- coding: utf-8 -*-
import scrapy
import re
import time
from FangSpider.items import FangspiderItem


class NewfangspiderSpider(scrapy.Spider):
    name = 'NewFangSpider'
    allowed_domains = ['fang.com']
    start_urls = [
        'http://newhouse.fang.com/house/s/c9y/',
        'http://newhouse.sh.fang.com/house/s/c9y/',
        'http://newhouse.gz.fang.com/house/s/c9y/',
        'http://newhouse.sz.fang.com/house/s/c9y/',
        'http://newhouse.dg.fang.com/house/s/c9y/',
        'http://newhouse.huizhou.fang.com/house/s/c9y/',
        'http://newhouse.fs.fang.com/house/s/c9y/',
        'http://newhouse.zs.fang.com/house/s/c9y/',
        'http://newhouse.zh.fang.com/house/s/c9y/',
        'http://newhouse.hz.fang.com/house/s/c9y/',
        'http://newhouse.tj.fang.com/house/s/c9y/']

    def parse(self, response):
        try:
            # print 'response.url:' + response.url
            loupanlist = response.xpath('//div[@class="contentList fl clearfix"]/ul[@class="flist"]')
            for i in xrange(1, len(loupanlist)):
                loupanurl = loupanlist[i - 1].xpath('./li[1]/div[@class="finfo c_333_f14"]/h3/a/@href').extract()[0]
                # print 'loupanurl:',loupanurl
                yield scrapy.Request(loupanurl, callback=self.parseLoupanInfo)
            baseurl = re.findall(re.compile(r'.*?com'), response.url)[0]
            if response.xpath('//div[@class="contentList fl clearfix"]/div[@id="sjina_D25_101"]/ul[@class="clearfix"]/li[@class="fr"]/a[@class="next"]/@href').extract() != []:
                nextpageurl = baseurl + response.xpath('//div[@class="contentList fl clearfix"]/div[@id="sjina_D25_101"]/ul[@class="clearfix"]/li[@class="fr"]/a[@class="next"]/@href').extract()[0]
                # print 'nextpageurl:' + nextpageurl
                yield scrapy.Request(nextpageurl, callback=self.parse)
        except Exception as e:
            print e

    def parseLoupanInfo(self,response):
        try:
            # print 'response.url:' + response.url
            items = FangspiderItem()
            items['EstateArea'] = re.findall(re.compile(u'(.*?)新房'),response.xpath('//div[@id="fyxq_B01_03"]/ul[@class="tf f12"]/li[2]/a/text()').extract()[0])[0]
            items['LouPanName'] = response.xpath('//div[@class="right_box"]/p[@id="fyxq_B01_05"]/a/text()').extract()[0]
            items['UnitNum'] = response.xpath('//div[@class="right_box"]/p[@id="fyxq_B01_05"]/strong/text()').extract()[0]
            items['RefPrice'] = response.xpath('//div[@class="right_box"]/div[@id="right_box_zj"]/p/span[2]').xpath('string(.)').extract()[0]
            items['AvePrice'] = response.xpath('//div[@class="right_box"]/div[@class="right_box_lpj"]/p/span[@class="cl_666"]/span/text()').extract()[0]
            sub =response.xpath('//div[@class="right_box"]/div[3]/div[@class="right_box_zzlxnr"]/ul[@class="right_box_zzlxnrl hidden"]/li[@class="f14"]')
            items['Mortgage'] = sub[0].xpath('string(.)').extract()[0]
            items['HuXing'] = sub[1].xpath('string(.)').extract()[0]
            items['LouDong'] = sub[2].xpath('string(.)').extract()[0]
            items['Floor'] = sub[3].xpath('string(.)').extract()[0]
            items['BuildCate'] = sub[4].xpath('string(.)').extract()[0]
            items['Area'] = response.xpath('//div[@class="right_box"]/div[3]/div[@class="right_box_zzlxnr"]/ul[@class="right_box_zzlxnrl hidden"]/li[@class="f14 w700"]/span[2]/a/text()').extract()[0]
            items['Street'] = response.xpath('//div[@class="right_box"]/div[3]/div[@class="right_box_zzlxnr"]/ul[@class="right_box_zzlxnrl hidden"]/li[@class="f14 w700"]/span[2]/a/text()').extract()[1]
            items['Position'] = response.xpath('//div[@class="right_box"]/div[3]/div[@class="right_box_zzlxnr"]/ul[@class="right_box_zzlxnrl hidden"]/li[@class="f14 w700"]/a/text()').extract()[0]
            items['Face'] = response.xpath('//div[@class="right_box"]/div[3]/div[@class="right_box_zzlxnr"]/div[@class="right_box_zzlxnrr_more"]/ul[1]/li[1]/text()').extract()[0]
            items['Unit'] = response.xpath('//div[@class="right_box"]/div[3]/div[@class="right_box_zzlxnr"]/div[@class="right_box_zzlxnrr_more"]/ul[1]/li[2]/text()').extract()[0]
            items['LouPanUrl'] = response.url
            items['CrawlTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print items['LouPanName']
        except Exception as e:
            print e
        finally:
            yield items 





