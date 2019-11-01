# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Join


class HouseListing(scrapy.Item):
    listing_url = scrapy.Field(output_processor=TakeFirst())  # Will be used as an ID, generically
    listing_type = scrapy.Field(output_processor=TakeFirst())  # 'Comprar' | 'Arrendar' | 'Ferias'
    title = scrapy.Field(output_processor=TakeFirst())
    house_location = scrapy.Field(output_processor=TakeFirst()) # This should be further parsed into City, Council and Parish
    house_cost = scrapy.Field(output_processor=TakeFirst())  # Depends on listing_type. It means: buying cost | cost per month | cost per week. Respectively.
    effective_area = scrapy.Field(output_processor=TakeFirst()) # "Area util"
    total_area = scrapy.Field(output_processor=TakeFirst())
    number_of_rooms = scrapy.Field(output_processor=TakeFirst())
    number_of_bathrooms = scrapy.Field(output_processor=TakeFirst())
    energy_certificate = scrapy.Field(output_processor=TakeFirst())
    house_condition = scrapy.Field(output_processor=TakeFirst())
    building_year = scrapy.Field(output_processor=TakeFirst())
    listing_description = scrapy.Field(output_processor=Join())
    house_characteristics = scrapy.Field() # Additional characteristics relevant to the house listing(Elevator? Garage? Garage place?)
    img_urls = scrapy.Field()
