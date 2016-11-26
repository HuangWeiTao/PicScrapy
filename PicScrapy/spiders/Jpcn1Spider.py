# -*- coding: utf-8 -*-
import logging
from PicScrapy.items import *
from PicScrapy.model.model import *
import re
from PicScrapy.repository.repository import PicRepository
from PicScrapy.model import downloadstatus
from urlparse import urlparse
from datetime import datetime

logging.basicConfig(filename='jpcn1.log', level=logging.INFO)

class Jpcn1TopicSpider(scrapy.Spider):
    name = "jpcn1-topic"

    def init_topic(self):
        topic_name = '街拍第一站 » 街拍丝足美足'
        start_url = 'http://www.jp95.com/' + 'forum-441-1.html'
        max_pages = 128

        repository = PicRepository()
        topic = repository.get_topic_by_name(topic_name)
        if topic == None:
            topic = Topic()
            topic.name = topic_name
            topic.start_url = start_url
            repository.save_topic(topic)

        return (topic,max_pages)

    def start_requests(self):
        topic, max_pages = self.init_topic()
        request = scrapy.Request(url=topic.start_url, callback=self.parse)
        request.meta['topic'] = topic
        request.meta['max_pages'] = max_pages
        yield request

    def parse(self, response):
        topic = response.meta['topic']
        max_pages = response.meta['max_pages']

        current_page = re.search('-(\d+).html', response.url)
        host = self.get_baseurl(response.url)+'/'
        post_list = response.css('#album a').xpath('@href').extract()
        for post_url in post_list:
            logging.info("saved post %s" % post_url)
            item = PostItem()
            item['url'] = host + post_url
            item['topic_id'] = topic.id
            yield item

        next_page = int(current_page.group(1))+1
        if(next_page>max_pages):
            return
        next_url = re.sub(r'-(\d+).html', '-'+str(next_page)+'.html',response.url)
        logging.info('next page %s' % next_url)
        request = scrapy.Request(url=next_url, callback=self.parse)
        request.meta['topic'] = topic
        request.meta['max_pages'] = max_pages
        yield request

    def get_baseurl(self, url):
        result = urlparse(url)
        baseurl = result.scheme+'://'+result.hostname
        if result.port!=None: #None represent 80 port
            baseurl = baseurl+':'+result.port
        return baseurl


class Jpcn1PostSpider(scrapy.Spider):
    name = 'jpcn1-post'

    def start_requests(self):
        return self.yield_requests()

    def yield_requests(self):
        repository = PicRepository()
        post_list = repository.get_unready_post(10)

        for post in post_list:
            post.status = downloadstatus.downloading
            repository.save_post(post)
            headers = self.get_auth_header(post.url)
            cookies = self.get_auth_cookies()
            request = scrapy.Request(url=post.url, cookies=cookies, headers=headers, callback=self.parse)
            request.meta['post'] = post
            yield request

    def parse(self,response):
        post = response.meta['post']
        html = response.body.decode('gbk')
        title = response.css('#threadtitle > h1::text').extract_first()
        img_list = response.css('img::attr(file)').extract()
        #with io.open('test.html','w',encoding='GBK') as f:
            #f.write(html)
        post.name = title
        post.status = downloadstatus.downloaded
        post.update_time = datetime.now()
        post_detail = {'post':post,'img_list':img_list}
        repository = PicRepository()
        repository.save_post_detail(post_detail)

        for img in img_list:
            logging.info('next page %s' % img)

        return self.yield_requests()

    def get_auth_cookies(self):
        cookies = {}
        cookies.update({'jpcn1netsid': '376VZy'})
        cookies.update({'jpcn1netoldtopics': 'D291081D'})
        cookies.update({'jpcn1netfid487': '1450800076'})
        cookies.update({'jpcn1netpic': '1'})
        cookies.update({'jpcn1netcookietime': '2592000'})
        cookies.update({'jpcn1netauth': '52a7clUi100bsbs3U9ttTSaSSCH2STcccfdcUp3r9aPCf%2BD1XP4MTo3CIBL5sblyt2myzrSdXTQ%2FG4t3r0HrZAgdC5JD'})
        cookies.update({'jpcn1netonlineusernum': '418'})
        cookies.update({'Hm_lvt_59ecce71bab2edc77b0acafa8ad73866': '1450800884'})
        cookies.update({'Hm_lpvt_59ecce71bab2edc77b0acafa8ad73866': '1450800913'})
        cookies.update({'smile': '1D1'})

        return cookies

    def get_auth_header(self,url):
        headers = {}
        headers.update({'Referer': self.get_baseurl(url)})
        headers.update({ 'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"})
        return headers

    def get_baseurl(self, url):
        result = urlparse(url)
        baseurl = result.scheme+'://'+result.hostname
        if result.port!=None: #None represent 80 port
            baseurl = baseurl+':'+result.port
        return baseurl