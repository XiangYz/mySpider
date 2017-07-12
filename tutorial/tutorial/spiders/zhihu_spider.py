import scrapy
import os
import urllib
import requests

class ZhihuSpider(scrapy.Spider):
	name = "Zhihu"
	start_urls = ['https://www.zhihu.com/question/27761934',]
	#start_urls = ['http://www.ibantang.com',]

	def parse(self, response):
		list_item = response.xpath("//div[@class='List-item']")
		for item in list_item:
			user = item.xpath(".//a[@class='UserLink-link']/text()").extract_first()
			img_list = item.xpath(".//img/@src").extract()
			i = 1
			for img_item in img_list:
				file_name = user + "_" + str(i) + ".jpg"
				file_path = os.path.join('D:\\xiang\\zhihu_pic', file_name)
				#urllib.urlretrieve(img_item, file_path)  #socket error
				"""
				urlopen = urllib.URLopener()
				fp = urlopen.open(img_item)
				imgdata = fp.read()
				fileobj = open(file_path, 'wb')
				fileobj.write(imgdata)
				fileobj.close()
				i = i + 1
				"""
				with requests.Session() as s:
					with open(file_path, "wb") as f:
					   f.write(s.get(img_item).content)
		
		
		"""
		i = 1
		for item in response.xpath("//div[@class='topic-item-v3']"):
			img_src = item.xpath(".//img/@data-original/text()").extract()
			
			for img_item in img_src:
				img_item_src = "www.ibantang.com" + img_item
				file_name = "img" + str(i)
				i = i + 1
				file_path = os.path.join('.\\ibantang_imgs', file_name)
				urllib.urlretrieve(img_item_src, file_path)
		"""