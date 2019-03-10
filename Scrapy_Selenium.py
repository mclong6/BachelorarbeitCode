from scrapy_selenium import SeleniumRequest
import scrapy
from scrapy.crawler import CrawlerProcess
from shutil import which
from bs4 import BeautifulSoup
import Personensuche_Bachelorarbeit

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
    def start_requests(self):
        Create_Search_Link=Personensuche_Bachelorarbeit.Create_Search_Link()
        url_list = Create_Search_Link.enter_information()
        print(url_list)
        urls = ['http://quotes.toscrape.com/page/2/', 'https://www.instagram.com/lamarcong']

        for url in urls:
            print("URL:  "+url)
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)
            #yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #print(response.request.meta['driver'].page_source)
        obj = BeautifulSoup(response.text, "html.parser")
        obj
        print(obj)

process = CrawlerProcess({
"user-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"
})
process.crawl(QuotesSpider)
process.start()
