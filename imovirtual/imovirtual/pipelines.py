# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/1latest/topics/item-pipeline.html


from w3lib.html import remove_tags
import re

class RemoveKeysWithNullValuesPipeline(object):
    """

    """

    def process_item(self, item, spider):
        new_item = {}

        for k, v in item.items():
            if v is not None:
                new_item[k] = v[0]

        return new_item


class HouseListingPipeline(object):
    """
        Determines if the house listing is 'Comprar' | 'Arrendar' | 'Ferias'
    """
    def process_item(self, item, spider):
        if 'listing_type' not in item:
            item['listing_type'] = 'buy'

        else:
            item['listing_type'] = ''.join(item['listing_type'])

            item['listing_type'] = item['listing_type'].lower().replace(' ', '')

            if item['listing_type'] == 'mês':
                item['listing_type'] = 'rent'

            elif item['listing_type'] == 'semana':
                item['listing_type'] = 'vacations'

        return item

class ExtractIntegersPipeline(object):
    """

    """

    __spider = None

    def open_spider(self, spider):
        self.__spider = spider

    def process_item(self, item, spider):
        self.extract_integer('building_year', item)
        self.extract_integer('effective_area', item)
        self.extract_integer('total_area', item)
        self.extract_integer('number_of_rooms', item)
        self.extract_integer('house_cost', item)

        return item

    def extract_integer(self, key, item):
        """
            Extracts the numbers from the specified string
        :param key: key to look for in the item's dictionary
        :param item: the item from which we will retrieve the value
        :return: integer or None
        """
        if key in item and item[key] is not None:
            item[key] = ''.join(item[key])
            # integers = [int(s) for s in item[key].split() if s.isdigit()]
            integers = re.findall(r'\d+', item[key].replace(' ', ''))

            if len(integers) == 1:
                # return integers[0]
                item[key] = integers[0]

            elif len(integers) > 1:
                self.__spider.logger.error("Found {} integers when expecting one for key: {} on item {}".format(
                    len(integers),
                    key,
                    str(item['listing_url'])
                ))


class ListingDescriptionPipeline(object):

    def process_item(self, item, spider):
        if 'listing_decription' in item:
            item['listing_description'] = remove_tags(item['listing_description'])

        return item