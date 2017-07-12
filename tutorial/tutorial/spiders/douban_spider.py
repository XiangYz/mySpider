import scrapy
import os
import urllib

from tutorial.items import DoubanMovieItem



class DoubanMovieTop250Spider(scrapy.Spider):
    name = 'douban_movie'
    #start_urls = ['https://movie.douban.com/top250']
    
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield scrapy.Request(url, headers = self.headers)
        

    def parse(self, response):
        
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)

        item = DoubanMovieItem()
        movies = response.xpath("//ol[@class='grid_view']/li")
        for movie in movies:
            item['ranking'] = movie.xpath(".//div[@class='pic']/em/text()").extract_first()
            item['movie_name'] = movie.xpath(".//div[@class='hd']/a/span[1]/text()").extract_first()
            item['score'] = movie.xpath(".//div[@class='star']/span[@class='rating_num']/text()").extract_first()
            item['score_num'] = movie.xpath(".//div[@class='star']/span[4]/text()").extract_first()
            yield item

        next_url = response.xpath("//span[@class='next']/a/@href").extract_first()
        if next_url:
            next_url = "https://movie.douban.com/top250" + next_url
            yield scrapy.Request(next_url, headers = self.headers)