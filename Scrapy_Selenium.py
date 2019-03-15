from scrapy_selenium import SeleniumRequest
import scrapy
from scrapy.crawler import CrawlerProcess
from shutil import which
from bs4 import BeautifulSoup
import Create_Search_Link_Class
import Keyword_Extraction_Class
import Gather_Information_Class
import re

all_keywords = []

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
        urls = ['https://www.google.com/search?q="Marco+Lang"+"Tettnang"+"1995"',
                'https://www.schwaebische.de/landkreis/bodenseekreis/tettnang_artikel,-junge-union-will-partty-bus-\
                verwirklichen-_arid,10701303.html']
        #urls = ["https://www.google.com/search?q=%22Marco+Lang%22+%22Tettnang%22"]
        for url in urls: #instead of urls, use url_list
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)
            #yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.request.meta['driver'].page_source)
        links_to_scrape = []
        obj = BeautifulSoup(response.text, "html.parser")
        result_div_list = obj.find_all("div", attrs={"class":"r"})

        #How do image results be handled?
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
        #self.gather_information()

        test_links = ['https://businesspf.hs-pforzheim.de/studium/studierende/bachelor/bw_einkauf_\
                        logistik/studierende/studentisches_leben/'
                      ]
        # for link in links_to_scrape:
        for link in test_links:
            yield SeleniumRequest(url=link, callback=self.gather_information, wait_time=10)

    def gather_information(self, response):
        #response = SeleniumRequest(url="https://www.schwaebische.de/landkreis/bodenseekreis/tettnang_artikel,"
                                      # "-junge-union-will-partty-bus-verwirklichen-_arid,10701303.html")
        #print(response)
        obj = BeautifulSoup(response.text, "html.parser")
        print("--------------------------------", response.url,"------------------------------------")
        keywword_extraction_class = Keyword_Extraction_Class.KeywordExtraction()
        formatted_string = keywword_extraction_class.formate_input_text(obj.body.text)
        keywords = keywword_extraction_class.create_keywords(formatted_string)
        keywords_string = "".join(keywords)

        with open("test.txt", "a") as myfile:
            myfile.write("\n"+response.url+"\n")
            myfile.write(keywords_string+"\n")

        #keywword_extraction_class.create_ngrams(keywords)

        gather_information_class = Gather_Information_Class.GatherInformation()
        gather_information_class.compare_keywords_with_databases(keywords)

process = CrawlerProcess({
"user-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"
})
process.crawl(QuotesSpider)
process.start()
