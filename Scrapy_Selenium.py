from scrapy_selenium import SeleniumRequest
import scrapy
from scrapy.crawler import CrawlerProcess
from shutil import which


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {
        'SELENIUM_DRIVER_NAME': 'chrome',
        'SELENIUM_DRIVER_EXECUTABLE_PATH' : which('/home/marco/Downloads/chromedriver'),
        'SELENIUM_DRIVER_ARGUMENTS' : ['--headless'],  # '--headless' if using chrome instead of firefox
        'DOWNLOADER_MIDDLEWARES' : {
        'scrapy_selenium.SeleniumMiddleware': 800
    }
    }
    """
    SELENIUM_DRIVER_NAME = 'chrome'
    SELENIUM_DRIVER_EXECUTABLE_PATH = which('/home/marco/Downloads/chromedriver')
    SELENIUM_DRIVER_ARGUMENTS = ['--headless']  # '--headless' if using chrome instead of firefox
    DOWNLOADER_MIDDLEWARES = {
        'scrapy_selenium.SeleniumMiddleware': 800
    }"""
    def start_requests(self):
        urls = [
            'https://www.instagram.com/lamarcong',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            print("test "+url)
            #yield scrapy.Request(url=url, callback=self.parse)
            #yield SeleniumRequest(url=url, callback=self.parse_result)
            yield SeleniumRequest(url=url, callback=self.parse_result)

    def parse_result(self, response):
        print(response.request.meta['driver'].page_source)

process = CrawlerProcess({
"user-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"
})
process.crawl(QuotesSpider)
process.start()
