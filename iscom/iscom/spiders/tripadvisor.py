# -*- coding: utf-8 -*-
import scrapy, functools, time
from bs4 import BeautifulSoup
from iscom.items import TripadvisorItem
from selenium import webdriver

class TripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    allowed_domains = ['www.tripadvisor.com.tw']
    start_urls = ['https://www.tripadvisor.com.tw/Attractions-g297910-Activities-oa{}-Taichung.html#ATTRACTION_LIST'.format(i) for i in range(0, 360, 30)]
    driver = webdriver.PhantomJS(executable_path='./phantomjs')

    def parse(self, response):
        self.driver.get(response.url)
        res = BeautifulSoup(self.driver.page_source)
        for i in res.select('.attraction_clarity_cell'):
            time.sleep(30)
            yield scrapy.Request('http://'+self.allowed_domains[0] + i.select('a')[0]['href'], self.parse_detail)

    def parse_detail(self, response):
        res = BeautifulSoup(response.body)
        tripItem = TripadvisorItem()
        tripItem['title'] = res.select('#HEADING')[0].text.replace('\n', '')
        tripItem['detail'] = [i.strip() for i in res.select('div.detail')[0].text.replace('\n', '').split(',')]
        tripItem['location'] = res.select('.colCnt2')[0].text if len(res.select('.colCnt2')) else ''
        tripItem['description'] = functools.reduce(lambda x,y:x+'\n'+y, map(lambda review:review.text, res.select('.partial_entry'))).replace('\n', '', 1).replace('More\xa0 \n', '')
        tripItem['image'] = res.select('.prw_rup.prw_common_centered_image.photo')[-1].select('img')[0]['src']
        tripItem['link'] = response.url
        return tripItem

