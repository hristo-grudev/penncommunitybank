import scrapy

from scrapy.loader import ItemLoader

from ..items import PenncommunitybankItem
from itemloaders.processors import TakeFirst


class PenncommunitybankSpider(scrapy.Spider):
	name = 'penncommunitybank'
	start_urls = ['https://www.penncommunitybank.com/press-releases/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="more-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="nav-previous"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=PenncommunitybankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
