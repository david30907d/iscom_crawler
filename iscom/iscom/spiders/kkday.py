# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from iscom.items import TripadvisorItem

class KkdaySpider(scrapy.Spider):
    name = 'kkday'
    allowed_domains = ['www.kkday.com']
    start_urls = ['https://www.kkday.com/zh-tw/product/productlist/A01-001?page={}&sort=hdesc'.format(i) for i in range(1, 32)]
    driver = webdriver.PhantomJS(executable_path='./phantomjs')

    def parse(self, response):
        self.driver.get(response.url)
        res = BeautifulSoup(self.driver.page_source)
        for i in res.select('.product-listview'):
            yield scrapy.Request(i.select('a')[0]['href'], self.parse_detail)

    def parse_detail(self, response):
        res = BeautifulSoup(response.body)
        tripItem = TripadvisorItem()
        tripItem['title'] = [i for i in [i.text.strip('\t').strip('\n').strip('\t') for i in res.select('.text-left')] if i]
        return tripItem
