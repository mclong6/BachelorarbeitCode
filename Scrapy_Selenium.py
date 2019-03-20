from scrapy_selenium import SeleniumRequest
import scrapy
from scrapy.crawler import CrawlerProcess
from shutil import which
from bs4 import BeautifulSoup
import Create_Search_Link_Class
import Keyword_Extraction_Class
import Gather_Information_Class
import re
import Create


class Person(object):
    def __init__(self):
        self.first_name = ""
        self.second_name = ""
        self.location = ""
        self.year_of_birth = ""
        self.instagram_name = ""
        self.facebook_name = ""
        self.institution = ""
        self.occupation = ""
        self.hobbies = ""
        self.universities = ""
        self.email = ""
        self.estimated_year_of_birth = ""


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
        url_list = create_search_link.get_search_links()
        print("URL-LIST: ", url_list)

        """url_list = ['https://www.google.com/search?q="Marco+Lang"+"Tettnang"+"1995"',
                'https://www.schwaebische.de/landkreis/bodenseekreis/tettnang_artikel,-junge-union-will-partty-bus-\
                verwirklichen-_arid,10701303.html']"""
        for url in url_list:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10, )

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
        next_page_links = []
        if next_page_tags: #check if list is not empty
            for links in next_page_tags:
                next_page_link = links.attrs['href']
                next_page_links.append(next_page_link)
            print("Further Pages: ", next_page_links)
            #TODO pages could be crawled
        else:
            print("No more pages to scrape!")
        # For testing
        test_links = ['https://businesspf.hs-pforzheim.de/studium/studierende/bachelor/bw_einkauf_\
                        logistik/studierende/studentisches_leben/'
                      ]
        # for link in links_to_scrape: # for real use
        for link in test_links:
            yield SeleniumRequest(url=link, callback=self.gather_information, wait_time=10)

    def gather_information(self, response):
        obj = BeautifulSoup(response.text, "html.parser")
        print("--------------------------------", response.url,"------------------------------------")
        keyword_extraction_class = Keyword_Extraction_Class.KeywordExtraction()
        formatted_string = keyword_extraction_class.formate_input_text(obj.body.text)
        keywords = keyword_extraction_class.create_keywords(formatted_string)

        gather_information_class = Gather_Information_Class.GatherInformation()
        person_object.hobbies = gather_information_class.compare_keywords_with_hobbies(keywords)
        person_object.locations = gather_information_class.compare_keywords_with_locations(keywords)
        person_object.universities = gather_information_class.compare_keywords_with_universities(keywords)
        person_object.occupation = gather_information_class.compare_keywords_with_occupations(keywords)
        person_object.email = gather_information_class.get_email(obj.body.text,person_object.first_name, person_object.second_name)

        print("Object" + person_object.first_name)
        print("Object" + person_object.second_name)
        print("Object" + person_object.location)
        print("Object" + person_object.year_of_birth)
        print("Object" + person_object.estimated_year_of_birth)
        print("Object" + person_object.institution)
        print("Object", person_object.email)




# transfer information from user input
def transfer_information():
    person_input_information = create_search_link.enter_information()
    person_object.first_name = person_input_information.first_name
    person_object.second_name = person_input_information.second_name
    person_object.location = person_input_information.location
    person_object.institution = person_input_information.institution
    person_object.year_of_birth = person_input_information.year_of_birth
    person_object.estimated_year_of_birth = person_input_information.estimated_year_of_birth


# Create Person object
create_search_link = Create_Search_Link_Class.CreateSearchLink()
person_object = Person()

transfer_information()



process = CrawlerProcess({
    "user-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"
})
process.crawl(QuotesSpider)
process.start()
