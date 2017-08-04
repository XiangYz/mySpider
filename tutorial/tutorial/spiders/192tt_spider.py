# -*- coding: utf-8 -*-

import scrapy
import os
import urllib
import urllib2
import imghdr
import requests
import re
import logging
from selenium import webdriver

class ZhihuSpider(scrapy.Spider):
    name = "192tt"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }


    def start_requests(self):
        url = 'http://www.192tt.com/gc/10qq/'
        req = scrapy.Request(url, headers = self.headers)
        #req.meta['PhantomJS'] = True
        yield req

    i = 1

    def parse(self, response):

        stop = False

        list_item = response.xpath("//div[@class='piclist']").xpath(".//li")
        for item in list_item:

            #publish_time = item.xpath(".//b[@class='b1']/text()").extract_first()
            #pub_time_list = publish_time.split('-')

            img_item = item.xpath(".//a/img/@src").extract_first()
            if not img_item:
                continue
            logging.info("---------------urllib2: " + img_item)
            

            img_req = urllib2.Request(img_item, headers=self.headers)
            content = None
            try:
                content = urllib2.urlopen(img_req).read()
            except:
                continue
            if not content:
                continue

            imgtype = imghdr.what('', h = content)
            if not imgtype:
                continue


            file_name = "192tt" + str(self.i)
            self.i = self.i + 1
            file_path = os.path.join('c:\\192tt_pic', file_name)
            
            with open(file_path + "." + imgtype, 'wb') as picfile:
                picfile.write(content)

            
        
        if not stop:   
            next_url = list_item.xpath("//div[@class='page']").xpath(".//a[@class='next']/@href").extract_first()
            if next_url:
                req = scrapy.Request(next_url, headers = self.headers)
                #req.meta['PhantomJS'] = True
                yield req
        