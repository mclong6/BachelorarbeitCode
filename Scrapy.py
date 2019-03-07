import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from bs4 import BeautifulSoup


class QuotesSpieder(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://www.instagram.com/lamarcong/"]

    def __init__(self):
        #super().__init__()
        self.driver = webdriver.Chrome("/home/marco/Downloads/chromedriver")


    def parse(self, response):
        self.driver.get(response.url)
        print(self.driver.page_source)
        self.driver.close()
process = CrawlerProcess({
"user-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"
})


process.crawl(QuotesSpieder())
process.start()
