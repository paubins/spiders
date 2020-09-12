# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.spiders import SitemapSpider
from books.items import SiteItem
import datetime
import os

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

class SpotifySpider(SitemapSpider):
    name = 'forloveandlemons.com'
    allowed_domains = ['forloveandlemons.com']
    sitemap_urls = ['https://forloveandlemons.com/robots.txt']
    sitemap_follow = ['sitemap.xml','sitemap_products_1.xml']
    slug_regex = re.compile("products\/(?P<slug>.*)")

    def parse(self, response):
        item = SiteItem()
        item['name'] = response.xpath("//meta[@property='og:title']/@content").extract_first()
        item['description'] = response.xpath("//meta[@property='og:description']/@content").extract_first()
        item['price'] = response.xpath("//meta[@property='og:price:amount']/@content").extract_first()
        url = response.xpath("//meta[@property='og:url']/@content").extract_first()
        item['url'] = response.request.url
        item['currency'] = response.xpath("//meta[@property='og:price:currency']/@content").extract_first()
        item['keywords'] = response.xpath("//meta[@name='keywords']/@content").extract_first()
        item['site_name'] = response.xpath("//meta[@property='og:site_name']/@content").extract_first()
        item['image_urls'] = [response.xpath("//meta[@property='og:image:secure_url']/@content").extract_first()]

        m = self.slug_regex.search(response.request.url)
        if m and m.groups():
            item['slug'] = m.group('slug')
            
        yield item


class HaperWilde(SpotifySpider):
    name = 'haperwilde.com'
    allowed_domains = ['haperwilde.com']
    sitemap_urls = ['https://haperwilde.com/robots.txt']


class SpotifySpider2(SpotifySpider):
    name = 'spotify_spider'

    def __init__(self, domain="", allowed_domains="", *args, **kwargs):
        super(SpotifySpider2, self).__init__(*args, **kwargs)
        self.allowed_domains = [allowed_domains]
        self.sitemap_urls = [os.path.join(domain, "robots.txt")]

class HaloTop(SitemapSpider):
    name = 'halotop.com'
    allowed_domains = ['halotop.com']
    sitemap_urls = ['https://halotop.com/robots.txt']
    sitemap_follow = ['sitemapper','sitemap_products_1.xml']
    slug_regex = re.compile("com\/(?P<slug>.*)")

    def parse(self, response):
        item = SiteItem()
        item['name'] = response.xpath("//meta[@property='og:title']/@content").extract_first()
        item['description'] = response.xpath("//meta[@property='og:description']/@content").extract_first()
        item['price'] = response.xpath("//meta[@property='og:price:amount']/@content").extract_first()
        url = response.xpath("//meta[@property='og:url']/@content").extract_first()
        item['url'] = response.request.url
        item['currency'] = response.xpath("//meta[@property='og:price:currency']/@content").extract_first()
        item['keywords'] = response.xpath("//meta[@name='keywords']/@content").extract_first()
        item['site_name'] = response.xpath("//meta[@property='og:site_name']/@content").extract_first()
        item['image_urls'] = [response.xpath("//meta[@property='og:image:secure_url']/@content").extract_first()]

        m = self.slug_regex.search(response.request.url)
        if m and m.groups():
            item['slug'] = m.group('slug')
            
        yield item
