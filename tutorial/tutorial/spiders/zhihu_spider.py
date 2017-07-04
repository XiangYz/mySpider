import scrapy
import os
import urllib

class ZhihuSpider(scrapy.Spider):
	name = "Zhihu"
	start_urls = ['https://www.zhihu.com/question/28047097',]


	def parse(self, response):
		for item in response.css("div.List-item"):
			user_name = item.css('a.UserLink-link::text').extract_first();
			img_src = item.css('img::attr(src)').extract();
			i = 1
			for img_item in img_src:
				img_item_src = "www.zhihu.com" + img_item
				file_name = user_name + "_" + str(i)
				file_path = os.path.join('.\\zhihu_spider', file_name)
				urllib.urlretrieve(img_item_src, file_path)

