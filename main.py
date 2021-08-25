import scrapy
from scrapy.crawler import CrawlerProcess

class BtrcspySpider(scrapy.Spider):
    name = 'btrcspy'
    start_urls = ['http://www.btrc.gov.bd/telco/mobile']


    def parse(self, response):

        for link in response.css("h2>a::attr(href)").getall():
            next_month = response.urljoin(link)
            yield scrapy.Request(url=next_month, callback=self.parse_details)

        if response.css("li.pager-next>a::attr(href)"):
            next_page = response.css("li.pager-next>a::attr(href)").get()
            next_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_link, callback=self.parse)



    def parse_details(self, response):
        # get a month's information table
        yield {
            'month': response.css("span.date-display-single::text").get(),
            'data': response.css("td>p ::text").extract()
        }

process = CrawlerProcess(settings={
    'FEED_URI': 'output.json',
    'FEED_FORMAT':'json'
})

process.crawl(BtrcspySpider)
process.start()