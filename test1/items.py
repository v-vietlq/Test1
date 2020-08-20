# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Test1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_id = scrapy.Field()
    link = scrapy.Field()
    Title = scrapy.Field()
    Author = scrapy.Field()
    Rate = scrapy.Field()
    Description = scrapy.Field()
    Reviews = scrapy.Field()
    pass
