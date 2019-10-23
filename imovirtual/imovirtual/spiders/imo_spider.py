import scrapy


class ImoSpider(scrapy.Spider):
    name = "imo"

    def start_requests(self):
        urls = [
            'https://www.imovirtual.com/comprar/apartamento/?page=4535',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('Hit parse')
        next_page_url = response.xpath('//*[@id="pagerForm"]/ul/li[7]/a')[0]
        print('Found next:', next_page_url)

        if next_page_url.attrib['class'] != 'disabled':
            yield scrapy.Request(next_page_url)
