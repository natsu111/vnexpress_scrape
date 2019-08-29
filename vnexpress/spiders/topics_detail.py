# -*- coding: utf-8 -*-
import scrapy
from vnexpress.items import VnexpressItem


class TopicsDetailSpider(scrapy.Spider):
    name = 'topics_detail'
    allowed_domains = ['vnexpress.net']
    start_urls = ['http://vnexpress.net/']

    def parse(self, response):
        for topic in response.css('section.sidebar_home_1 > article.list_news > h4'):
            item = VnexpressItem()
            item['title'] = topic.css('a::text').extract_first()
            yield scrapy.Request(topic.css('a::attr(href)').extract_first(),
                                 callback=self.parse_detail,
                                 meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item']
        item['subtitle'] = response.css(
            'p.description::text').extract_first()
        item['content'] = response.xpath(
            '//article/p[@class="Normal"]/text()').extract()
        item['category'] = response.css('li.start > h4 > a::text').extract()
        yield item


# response.css('section.sidebar_1 > article > p.Normal').extract()
# response.xpath('//article/p[@class="Normal"]/text()').extract()
#  article.list_news > h4
# body > section:nth-child(8) > section.sidebar_home_1 > article:nth-child(1) > h4 > a:nth-child(1)
