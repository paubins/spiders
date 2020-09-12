# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import os
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline

from pgpipeline import PgPipeline

import datetime

BRAND_ID = 100
USER_ID = 13 # paubins

class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not adapter.get('slug'):
        	raise DropItem("Duplicate item found: %r" % item)

        if adapter['slug'] in self.ids_seen:
            raise DropItem("Duplicate item found: %r" % item)
        else:
            self.ids_seen.add(adapter['slug'])
            return item

class ParseImagesPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter['image'] = image_paths[0]

        for image_path in image_paths:
        	medium_image_path = os.path.join("thumbs", image_path.replace("full", "medium"))
        	small_image_path = os.path.join("thumbs", image_path.replace("full", "small"))
        	item["logo_url"] = f"http://shi2.s3-us-west-1.amazonaws.com/images/{small_image_path}"
        	item["main_photo_url"] = f"http://shi2.s3-us-west-1.amazonaws.com/images/{medium_image_path}"
        	item["image1"] = f"http://shi2.s3-us-west-1.amazonaws.com/images/{image_path}"
        	break
        	
        return item

class PairingPipeline(PgPipeline):
	def process_item(self, item, spider):
		item['user_id'] = USER_ID
		item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		item['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		item = super(PairingPipeline, self).process_item(item, spider)
		product = self.table.find_one(slug=item["slug"])
		pairings_table = self.db["pairings"]
		pairings_table.upsert(dict(
			product_id=product["id"],
			brand_id=BRAND_ID,
			user_id=USER_ID,
			source=item["url"],
			description=item["site_name"],
			created_at=item['created_at'],
			updated_at=item['updated_at']), ['brand_id', 'product_id'])

		tags_table = self.db["tags"]
		if item["keywords"]:
			tags = item["keywords"].split(" ")
			tags_table = self.db["tags"]
			taggings_table = self.db["taggings"]
			for tag in tags:
				tags_table.upsert(dict(name=tag), ['name'])
				current_tag = tags_table.find_one(name=tag)

				taggings_table.upsert(dict(
					tag_id=current_tag["id"],
					taggable_type="Product",
					taggable_id=product["id"],
					tagger_table="User",
					tagger_id=USER_ID,
					context="tags"
					), ["tag_id", "taggable_id"])
		return item
