import scrapy
import os
import urllib
import urllib2
import imghdr
import requests
import re

class ZhihuSpider(scrapy.Spider):
    name = "jiandan"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }


    def start_requests(self):
        url = 'http://jandan.net/ooxx'
        yield scrapy.Request(url, headers=self.headers)

    i = 1

    def parse(self, response):
        list_item = response.xpath("//ol[@class='commentlist']/li")
        for item in list_item:

            img_item = item.xpath(".//img/@src").extract_first()
            if not img_item:
                continue
            pos = img_item.rfind('.gif')
            if pos > 0:
                img_item = item.xpath(".//img/@org_src").extract_first()
                if not img_item:
                    continue
            file_name = "jiandan_" + str(self.i)
            self.i = self.i + 1
            file_path = os.path.join('D:\\xiang\\github_space\\jiandan_pic', file_name)
            content = urllib2.urlopen("http:" + img_item).read()

            if not content:
                continue
            imgtype = imghdr.what('', h = content)
            if not imgtype:
                continue
            
            with open(file_path + "." + imgtype, 'wb') as picfile:
                picfile.write(content)

            

        next_url = response.xpath("//div[@class='cp-pagenavi']/a[@class='previous-comment-page']/@href").extract_first()
        if next_url:
            yield scrapy.Request(next_url, headers = self.headers)