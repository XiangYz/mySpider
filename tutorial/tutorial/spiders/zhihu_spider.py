import scrapy
import os
import urllib

class ZhihuSpider(scrapy.Spider):
	name = "Zhihu"
	#start_urls = ['https://www.zhihu.com/question/27761934',]
	start_urls = ['http://www.ibantang.com',]

	def parse(self, response):
		"""
		for item in response.xpath("//div[@class='List-item']"):
			user_name = item.xpath("//a[@class='UserLink-link']/text()").extract_first()
			img_src = item.xpath("//img/@src/text()").extract()
			
			i = 1
			for img_item in img_src:
				img_item_src = "www.zhihu.com" + img_item
				file_name = user_name + "_" + str(i)
				file_path = os.path.join('.\\zhihu_spider', file_name)
				urllib.urlretrieve(img_item_src, file_path)
		"""
		
		i = 1
		for item in response.xpath("//div[@class='topic-item-v3']"):
			img_src = item.xpath("//img/@data-original/text()").extract()
			
			for img_item in img_src:
				img_item_src = "www.ibantang.com" + img_item
				file_name = "img" + str(i)
				i = i + 1
				file_path = os.path.join('.\\ibantang_imgs', file_name)
				urllib.urlretrieve(img_item_src, file_path)


