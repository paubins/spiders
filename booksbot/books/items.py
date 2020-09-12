# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SiteItem(scrapy.Item):
	name = scrapy.Field()
	description = scrapy.Field()
	price = scrapy.Field()
	url = scrapy.Field()
	currency = scrapy.Field()
	availability = scrapy.Field()
	keywords = scrapy.Field()
	slug = scrapy.Field()
	site_name = scrapy.Field()
	image_urls = scrapy.Field()
	image = scrapy.Field()
	created_at = scrapy.Field()
	updated_at = scrapy.Field()
	user_id = scrapy.Field()
	main_photo_url = scrapy.Field()
	image1 = scrapy.Field()
	logo_url = scrapy.Field()
