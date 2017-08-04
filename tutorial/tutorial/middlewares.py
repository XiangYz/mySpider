# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


import functools
import json
import time
import logging

from selenium import webdriver
from scrapy.conf import settings
from scrapy.http import HtmlResponse

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher 
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.remote_connection import LOGGER
from telnetlib import DO



LOGGER.setLevel(logging.INFO)

#set phantomJS's agent to Firefox
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = \
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"


class PhantomJSMiddleware(object):

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

    scrollToBottom()
    '''

    def process_request(self, request, spider):
        if spider.name == "192tt":
            logging.info("--------------PhantomJS is starting")
            driver = webdriver.PhantomJS(executable_path=settings['JS_BIN']) #指定使用的浏览器
            logging.info("--------------" + request.url)
            driver.get(request.url)
            #time.sleep(1)
            js1 = 'return document.body.scrollHeight'
            js2 = "window.scrollTo(0, document.body.scrollHeight)" 
            old_scroll_height = 0
            while(driver.execute_script(js1) > old_scroll_height):
                old_scroll_height = driver.execute_script(js1)
                driver.execute_script(js2)
                time.sleep(3)
            #driver.execute_script(js1) #可执行js，模仿用户操作。此处为将页面拉至最底端。       
            #time.sleep(3)
            body = driver.page_source
            cur_url = driver.current_url
            driver.quit()
            logging.info("----------------got " + cur_url)
            return HtmlResponse(cur_url, body=body, encoding='utf-8', request=request)



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








