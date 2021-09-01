import scrapy
from scrapy.crawler import CrawlerProcess


class BtrcspySpider(scrapy.Spider):
    # naming the spider defining baseurl
    name = 'btrcspy'
    start_urls = ['http://www.btrc.gov.bd/telco/mobile']

    def parse(self, response):
        # baseurl loaded
        # page contains table with monthly dates and links

        for link in response.css("h2>a::attr(href)").getall():                     # iterate & collect monthly table root links
            next_month = response.urljoin(link)                                    # joins root link with baseurl
            yield scrapy.Request(url=next_month, callback=self.parse_details)      # goes to link and runs parse_details

        if response.css("li.pager-next>a::attr(href)"):                            # check for next page nav link
            next_page = response.css("li.pager-next>a::attr(href)").get()          # get nav link if available
            next_link = response.urljoin(next_page)                                # join nav link with baseurl
            yield scrapy.Request(url=next_link, callback=self.parse)               # go to next page if next page link available

    def parse_details(self, response):
        # redirected to inside monthly table
        # parse data from monthly information table
        yield {
            'month': response.css("span.date-display-single::text").get(),
            'data': response.css("td>p ::text").extract()
        }


# config below needed to use spider as a single py script
# FEED URI is the name of the output file incld. type
# FEED FORMAT is the desired output format
process = CrawlerProcess(
    settings={
        'FEED_URI': 'output.json',
        'FEED_FORMAT': 'json'
    })


process.crawl(BtrcspySpider)            # pass spider class
process.start()                         # run script
