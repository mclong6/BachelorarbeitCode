from scrapy_selenium import SeleniumRequest
import scrapy
from scrapy.crawler import CrawlerProcess
from shutil import which
from bs4 import BeautifulSoup
import Create_Search_Link_Class
import re


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
        #For link-creation
        """create_search_link = Create_Search_Link_Class.CreateSearchLink()
        url_list = create_search_link.enter_information()
        print("URL-LIST: ", url_list)
        """
        urls = ['https://www.google.com/search?q="Marco+Lang"+"Tettnang"+"1995"']
        #urls = ["https://www.google.com/search?q=%22Marco+Lang%22+%22Tettnang%22"]
        for url in urls: #instead of urls, use url_list
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)
            #yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.request.meta['driver'].page_source)
        links_to_scrape = []
        obj = BeautifulSoup(response.text, "html.parser")
        result_div_list = obj.find_all("div", attrs={"class":"r"})

        for result_div in result_div_list:
            a_tag = result_div.find("a", attrs={'href': re.compile("^.*")})
            links_to_scrape.append(a_tag.attrs['href'])
        print("Links:", links_to_scrape)

        next_page_tags = obj.find_all("a", attrs={'aria-label': re.compile("^(Page )[0-9]{1,3}")})
        print(next_page_tags)

        if next_page_tags: #check if list is not empty
            for links in next_page_tags:
                next_page_links = links.attrs['href']
                print(next_page_links)
                #TODO pages could be crawled
        else:
            print("No more pages to scrape!")

        #TODO links_to_scrape must be scraped


process = CrawlerProcess({
"user-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"
})
process.crawl(QuotesSpider)
process.start()
