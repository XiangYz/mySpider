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
        yield scrapy.Request(url, headers=self.headers)

    i = 1

    def parse(self, response):

        stop = False

        list_item = response.xpath("//div[@class='piclist']").xpath(".//li")
        for item in list_item:

            publish_time = item.xpath(".//b[@class='b1']/text()").extract_first()
            pub_time_list = publish_time.split('-')


            img_item = item.xpath(".//a/img/@src").extract_first()
            if not img_item:
                continue

            file_name = "192tt" + str(self.i)
            self.i = self.i + 1
            file_path = os.path.join('C:\\192tt_pic', file_name)
            content = urllib2.urlopen(img_item).read()

            if not content:
                continue
            imgtype = imghdr.what('', h = content)
            if not imgtype:
                continue
            
            with open(file_path + "." + imgtype, 'wb') as picfile:
                picfile.write(content)
        '''
        if not stop:   
            next_url = response.xpath("//div[@class='cp-pagenavi']/a[@class='previous-comment-page']/@href").extract_first()
            if next_url:
                yield scrapy.Request(next_url, headers = self.headers)
        '''