import scrapy
import os
import urllib
import re
import json
import imghdr
import urllib
import urllib2



class BantangAjax(scrapy.Spider):
    name = 'bantang_ajax'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'http://www.ibantang.com/topic/getHomeTopicList?type=topic_main&extend=&page=1&pagesize=30'
        yield scrapy.Request(url, headers=self.headers)

    index = 1
    def parse(self, response):
        datas = json.loads(response.body)
        if datas:
            
            for data in datas['data']['topic']:
                pic = data['pic']
                content = urllib2.urlopen(pic).read()
                imgtype = imghdr.what('', h=content)
                file_name = "bantang_" + str(self.index)
                self.index = self.index + 1
                file_path = os.path.join('D:\\xiang\\github_space\\bantang_pic', file_name)
                if not imgtype:
                    imgtype = 'txt'
                with open(file_path + "." + imgtype, 'wb') as f:
                    f.write(content)
            
            page_num = re.search(r'page=(\d+)', response.url).group(1)
            page_num = 'page=' + str(int(page_num)+1)
            next_url = re.sub(r'page=\d+', page_num, response.url)
            yield scrapy.Request(next_url, headers=self.headers)