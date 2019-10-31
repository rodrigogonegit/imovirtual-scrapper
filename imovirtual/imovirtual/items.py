# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseListing(scrapy.Item):
    listing_url = scrapy.Field()  # Will be used as an ID, generically
    listing_type = scrapy.Field()  # 'Comprar' | 'Arrendar' | 'Ferias'
    title = scrapy.Field()
    house_location = scrapy.Field() # This should be further parsed into City, Council and Parish
    house_cost = scrapy.Field()  # Depends on listing_type. It means: buying cost | cost per month | cost per week. Respectively.
    effective_area = scrapy.Field() # "Area util"
    total_area = scrapy.Field()
    number_of_rooms = scrapy.Field()
    number_of_bathrooms = scrapy.Field()
    energy_certificate = scrapy.Field()
    house_condition = scrapy.Field()
    building_year = scrapy.Field()
    listing_description = scrapy.Field()
    house_characteristics = scrapy.Field() # Additional characteristics relevant to the house listing(Elevator? Garage? Garage place?)

