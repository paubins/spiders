# -*- coding: utf-8 -*-

BOT_NAME = 'books'

SPIDER_MODULES = ['books.spiders']
NEWSPIDER_MODULE = 'books.spiders'

ROBOTSTXT_OBEY = True
HTTPCACHE_ENABLED = True

ITEM_PIPELINES = {
	'books.pipelines.DuplicatesPipeline': 100,
	'books.pipelines.ParseImagesPipeline': 300,
	'books.pipelines.PairingPipeline': 400,
}

PG_PIPELINE = {
    'connection': 'postgresql://ufbivs448r9cld:pf12a43043cf88b2d44ba0e4242e4c479f4178e83b0c09f24fb25e33e6eba7bc8@ec2-35-169-44-206.compute-1.amazonaws.com:5432/d1b202fii8499b',
    'table_name': 'products',
    'pkey' : 'slug',
    'ignore_identical': ['slug'],
    'onconflict': 'upsert'
}

IMAGES_THUMBS = {
    'small': (70, 70),
    'medium': (200, 200),
}