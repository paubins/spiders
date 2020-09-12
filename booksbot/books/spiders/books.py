# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.spiders import SitemapSpider
from books.items import SiteItem
import datetime

class StoriesProductSpider(SitemapSpider):
    name = 'stories.com'
    allowed_domains = ['stories.com']
    sitemap_urls = ['http://www.stories.com/robots.txt']
    sitemap_follow = ['en.sitemap.xml','en.product.0.xml']
    slug_regex = re.compile("product\.(?P<slug>.*)\.[0-9]+\.html")

    def parse(self, response):
        item = SiteItem()
        item['name'] = response.xpath("//html/head/meta[@property='og:title']/@content").extract_first()
        item['description'] = response.xpath("//html/head/meta[@property='og:description']/@content").extract_first()
        item['price'] = response.xpath("//html/head/meta[@property='og:price:amount']/@content").extract_first()
        url = response.xpath("//html/head/meta[@property='og:url']/@content").extract_first()
        item['url'] = url
        item['currency'] = response.xpath("//html/head/meta[@property='og:price:currency']/@content").extract_first()
        item['keywords'] = response.xpath("//html/head/meta[@name='keywords']/@content").extract_first()
        item['site_name'] = response.xpath("//html/head/meta[@property='og:site_name']/@content").extract_first()

        image_url = response.xpath("//source[@media='(min-width:1951px)']/@srcset").extract_first()
        if image_url:
            item['image_urls'] = ["http:" + image_url]

        m = self.slug_regex.search(url)
        if m and m.groups():
            item['slug'] = m.group('slug')
            
        yield item

