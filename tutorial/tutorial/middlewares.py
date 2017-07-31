# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


import functools
import json
import multiprocessing.context
import multiprocessing.pool

from selenium import webdriver
from scrapy.conf import settings
# from scrapy.http.response import Response
from scrapy.http import HtmlResponse
import time
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher 
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.remote_connection import LOGGER
from telnetlib import DO
import logging


LOGGER.setLevel(logging.INFO)

def timeout(max_timeout):
    '''
    Timeout decorator, parameter in seconds.
    http://stackoverflow.com/a/35139284/7035932
    '''
    def timeout_decorator(item):
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator

logger = logging.getLogger(__name__)

def getresponse(driver):
    log = driver.get_log('har')
    log = json.loads(log[0]['message'])
    return log['log']['entries'][0]['response']


class PhantomJSMiddleware(object):

    def __init__(self):
        self.driver = None

    def __del__(self):
        if self.driver:
            self.driver.quit()

    def injectheaders(self, headers):
        caps = DesiredCapabilities.PHANTOMJS.copy()
        caps['phantomjs.page.settings.loadImages'] = True
        # caps['proxy'] = proxy json object
        # https://github.com/SeleniumHQ/selenium/wiki/DesiredCapabilities#proxy-json-object
        if 'User-Agent' in headers:
            caps['phantomjs.page.settings.UserAgent'] = headers['User-Agent']
            del headers['User-Agent']
        for key in headers:
            caps['phantomjs.page.customheaders.' + key] = headers[key]
        self.driver.start_session(caps)

    @timeout(10)
    def _process_request(self, request, spider):
        driver = self.driver
        headers = request.headers.to_unicode_dict()
        encoding = request.encoding
        self.injectheaders(headers)
        driver.get(request.url)
        isnotloaded = True
        while isnotloaded:
            time.sleep(0.1)
            try:
                response = getresponse(driver)
                if response['status']:
                    isnotloaded = False
            except IndexError:
                pass
        body = driver.page_source
        status_code = response['status']
        headers = [(x['name'], x['value']) for x in response['headers']]
        return HtmlResponse(driver.current_url, body=body,
                            status=status_code, headers=headers,
                            encoding=encoding, request=request)

    def process_request(self, request, spider):
        if self.driver is None:
            self.driver = webdriver.PhantomJS()
        if request.method != 'GET':
            raise NotImplementedError(
                'Do not support {r.method} method'.format(r=request))
        isnotworking = True
        while isnotworking:
            try:
                return self._process_request(request, spider)
            except multiprocessing.context.TimeoutError:
                logger.warning('Timeout ...')
            except Exception as e:
                msg = str(e).strip()
                if msg:
                    logger.error(msg)
            logger.info('restart process_request')
            self.driver.quit()
            self.driver = webdriver.PhantomJS()



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








