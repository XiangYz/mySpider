# -*- coding: utf-8 -*-

import scrapy
import os
import urllib
import re
import json

from tutorial.items import DoubanMovieItem



class DoubanAjax(scrapy.Spider):
    name = 'douban_ajax'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/\
        537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://movie.douban.com/j/chart/top_list?type=5&\
        interval_id=100%3A90&action=&start=0&limit=20'
        yield scrapy.Request(url, headers=self.headers)

    def parse(self, response):
        #运行后response为空
        datas = json.loads(response.body)
        item = DoubanMovieItem()
        if datas:
            for data in datas:
                item['ranking'] = data['rank']
                item['movie_name'] = data['title']
                item['score'] = data['score']
                item['score_num'] = data['vote_count']
                yield item

            
            page_num = re.search(r'start=(\d+)', response.url).group(1)
            page_num = 'start=' + str(int(page_num)+20)
            next_url = re.sub(r'start=\d+', page_num, response.url)
            yield scrapy.Request(next_url, headers=self.headers)