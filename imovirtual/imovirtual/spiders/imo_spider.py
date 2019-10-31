import scrapy
import unicodedata
from scrapy.loader import ItemLoader
from imovirtual.items import HouseListing


class ImoSpider(scrapy.Spider):
    name = "imo"

    def start_requests(self):
        """
            Entry point of the class
        :return: returns a list of HouseListing
        """
        self.logger.info("Hit start_requests")
        urls = [
            'https://www.imovirtual.com/comprar/apartamento/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
            Iterates through all the Housing Ad URLs found and processes them.
            It's possible to choose between 24, 48 or 72 listings per page.
        :param response: scrapy HTTP response to be used within this context
        :return: returns a list of HouseListing
        """
        self.logger.debug("Hit parse")
        item_details_links = [d.attrib['href'] for d in response.css('div.offer-item-details-bottom > ul > a')]

        # Iterate through every listing
        for url in item_details_links:
            yield scrapy.Request(url=url, callback=self.parse_listing)

        # Check if there is a next page
        next_page_url = response.css('#pagerForm > ul > li.pager-next > a')

        if len(next_page_url) == 1:
            next_page_url = next_page_url[0]

            if 'class' in next_page_url.attrib and next_page_url.attrib['class'] != 'disabled':
                self.logger.info('Found next page: {}'.format(next_page_url.attrib['href']))
                yield scrapy.Request(next_page_url.attrib['href'])
        else:
            self.logger.debug("Could not find next page")

    def parse_listing(self, response):
        """
            Parses the actual housing listing.
        :rtype: HouseListing
        :param response: scrapy HTTP response to be used within this context
        :return: returns one HouseListing
        """
        ul_list = response.xpath('//*[@id="root"]/article/div[3]/div[1]/section[1]/div/ul')[0]
        # #root > article > div.css-o19mot-Te > div.css-18jo4jf-Te > section.section-overview > div > ul

        l = ItemLoader(item=HouseListing(), response=response)
        l.add_value('listing_url', response.url)
        l.add_css('listing_type', '#root > article > header > div.css-s3teq > div.css-13ywf6 > div.css-1vr19r7 > small::text')
        l.add_css('title', '#root > article > header > div.css-1jiadof > div > div > h1::text')
        l.add_css('house_location', '#root > article > header > div.css-1jiadof > div > div > div > a::text')
        l.add_css('house_cost', '#root > article > header > div.css-s3teq > div.css-13ywf6 > div.css-1vr19r7::text')

        # Order of listing features (Propriedades as the website calls it) is not guaranteed. Must check the label name.
        l.add_value('effective_area', self.find_matching_field_value('area util', ul_list))
        l.add_value('total_area', self.find_matching_field_value('area bruta', ul_list))
        l.add_value('number_of_rooms', self.find_matching_field_value('tipologia', ul_list))
        l.add_value('number_of_bathrooms', self.find_matching_field_value('casas de banho', ul_list))
        l.add_value('energy_certificate', self.find_matching_field_value('certificado energetico', ul_list))
        l.add_value('house_condition', self.find_matching_field_value('condicao', ul_list))
        l.add_value('building_year', self.find_matching_field_value('ano de construcao', ul_list))

        l.add_xpath('listing_description', '//*[@id="root"]/article/div[3]/div[1]/section[2]/div[1]')
        l.add_xpath('house_characteristics', '//*[@id="root"]/article/div[3]/div[1]/section[3]/div/ul//text()')
        # print("-------------")
        # print(str(l))
        return l.load_item()

    def find_matching_field_value(self, imovirtual_label_name: str, li_list: scrapy.Selector) -> str:
        """
            Finds the corresponding value of a HouseListing field given the ImoVirtual label name and the whole list
        :rtype: str
        :param imovirtual_label_name: the corresponding label name from the "Propriedades" list on the
        website. The property must be given in an ASCII compliant string
        :param li_list: the list as a
        scrapy.Selector object (to avoid finding it every time the function is called
        """

        for p in li_list.css('li'):
            label_name = unicodedata.normalize('NFKD', p.css('::text').get()).encode('ascii', 'ignore').decode('utf-8')

            if imovirtual_label_name.lower() in label_name.lower():
                return p.css('strong::text').get()

        return ""

if __name__ == "__main__":
    # execute only if run as a script
    s = ImoSpider()