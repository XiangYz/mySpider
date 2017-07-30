# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from selenium import webdriver
from scrapy.conf import settings
# from scrapy.http.response import Response
from scrapy.http import HtmlResponse
import time
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher 
from telnetlib import DO
import logging


class TutorialSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        pass








class JavaScriptMiddleware(object):
    '''
    def __init__(self):
        self.driver = webdriver.PhantomJS(executable_path=settings['JS_BIN'])
    '''
    
    def process_request(self, request, spider):

        js = '''
        function scrollToBottom() {

            var Height = document.body.clientHeight,  //文本高度
            screenHeight = window.innerHeight,  //屏幕高度
            INTERVAL = 100,  // 滚动动作之间的间隔时间
            delta = 500,  //每次滚动距离
            curScrollTop = 0;    //当前window.scrollTop 值

            var scroll = function () {
                curScrollTop = document.body.scrollTop;
                window.scrollTo(0,curScrollTop + delta);
            };

            var timer = setInterval(function () {
                var curHeight = curScrollTop + screenHeight;
                if (curHeight >= Height){   //滚动到页面底部时，结束滚动
                    clearInterval(timer);
            }
            
            scroll();
            }, INTERVAL)
        }

        '''

        if request.meta.has_key('PhantomJS'):
            driver = webdriver.PhantomJS(executable_path=settings['JS_BIN']) 
            driver.get(request.url)
            logging.info("-----------------" + str(request.url) + "-----------------")
            logging.info("-----------------" + str(driver.current_url) + "-----------------")
            time.sleep(1)
            js = "var q=document.documentElement.scrollTop=10000"
            driver.execute_script(js)   
            time.sleep(2)  # 等待JS执行

            content = driver.page_source.encode('utf-8')
            driver.quit()  
            return HtmlResponse(driver.current_url, encoding='utf-8', body=content, request=request)


        '''
        self.driver.get(request.url)
        logging.info("page rendering, auto pulling down...")
        indexPage = 1000
        while indexPage < self.driver.execute_script("return document.body.offsetHeight"):
            self.driver.execute_script("scroll(0,"+str(indexPage)+")")
            indexPage = indexPage +1000
            logging.info(indexPage)
            time.sleep(1)

        rendered_body = self.driver.page_source
        #编码处理
        if r'charset="GBK"' in rendered_body or r'charset=gbk' in rendered_body:
            coding = 'gbk'
        else:
            coding = 'utf-8'
        return HtmlResponse(request.url, body=rendered_body, encoding='utf-8')
        '''

    #关闭浏览器
    def spider_closed(self, spider, reason):
        logging.info ('-------------------driver closing----------------------')
        self.driver.close()