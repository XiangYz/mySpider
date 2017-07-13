import scrapy
import os
import urllib
import urllib2
import imghdr
import requests
import re

class ZhihuSpider(scrapy.Spider):
    name = "Zhihu"
    #start_urls = ['https://www.zhihu.com/question/27761934',]
    #start_urls = ['http://www.ibantang.com',]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }


    def start_requests(self):
        url = 'https://www.zhihu.com/question/37787176'
        yield scrapy.Request(url, headers=self.headers)

    def parse(self, response):
        list_item = response.xpath("//div[@class='List-item']")
        for item in list_item:
            user = item.xpath(".//a[@class='UserLink-link']/text()").extract_first()
            content_list = item.xpath(".//div[@class='RichContent-inner']")
            img_list = content_list.xpath(".//img/@src").extract()
            i = 1
            for img_item in img_list:
                res = re.search(r"whitedot", img_item)
                if res:
                    continue

                file_name = user + "_" + str(i)
                i = i + 1
                file_path = os.path.join('D:\\xiang\\github_space\\zhihu_pic', file_name)
                content = urllib2.urlopen(img_item).read()
                imgtype = imghdr.what('', h = content)
                if not imgtype:
                    imgtype = 'txt'
                with open(file_path + "." + imgtype, 'wb') as f:
                    f.write(content)
