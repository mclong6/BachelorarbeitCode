from scrapy_selenium import SeleniumRequest
import scrapy
from scrapy.crawler import CrawlerProcess
from shutil import which
from bs4 import BeautifulSoup
import Create_Search_Link_Class
import Keyword_Extraction_Class
import Gather_Information_Class
import Social_Media_Class
import re


class Person(object):
    def __init__(self):
        self.first_name = input("Vorname: ").replace(" ", "%22")
        self.second_name = input("Nachname: ").replace(" ", "%22")
        self.place_of_residence = input("Wohnort: ").replace(" ", "%22")
        self.year_of_birth = input("Genaues Geburtsjahr: ").replace(" ", "%22")
        self.estimated_year_of_birth = input("Geschätztes Geburtsjahr: ").replace(" ", "%22")
        self.institution = input("Institution: ").replace(" ", "%22")
        self.instagram_name = input("Instagram Benutzername: ")
        # self.facebook_name = input("Facebook Benutzername: ")
        # self.twitter_name = input("Twitter Benutzername")
        self.occupation = []
        self.hobbies = []
        self.universities = []
        self.email = []
        self.locations = []

        """self.first_name = ""
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
        self.estimated_year_of_birth = """""


class QuotesSpider(scrapy.Spider):
    def __init__(self):
        self.name = "quotes"
        self.custom_settings = {
            'SELENIUM_DRIVER_NAME': 'chrome',
            'SELENIUM_DRIVER_EXECUTABLE_PATH' : which('/home/marco/Downloads/chromedriver'),
            'SELENIUM_DRIVER_ARGUMENTS' : ['--headless'],  # '--headless' if using chrome instead of firefox
            'DOWNLOADER_MIDDLEWARES' : {
            'scrapy_selenium.SeleniumMiddleware': 800
            }
        }
        self.instagram_key = 1
        self.facebook_key = 2
        self.twitter_key = 3

    def start_requests(self):
        #For link-creation
        social_media = Social_Media_Class.SocialMedia()
        if person_object.instagram_name:
            social_media.login_to_any_page(self.instagram_key)
            response = social_media.search_instagram(person_object.instagram_name)
            self.gather_information(response)
        create_search_link = Create_Search_Link_Class.CreateSearchLink()
        url_list = create_search_link.get_search_links(person_object)
        print("URL-LIST: ", url_list)
        """url_list = ['https://www.google.com/search?q="Marco+Lang"+"Tettnang"+"1995"',
                'https://www.schwaebische.de/landkreis/bodenseekreis/tettnang_artikel,-junge-union-will-partty-bus-\
                verwirklichen-_arid,10701303.html']"""
        for url in url_list:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)

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
        #test_links = ['http://www.internetlivestats.com/total-number-of-websites/']
        test_links = ['https://www.instagram.com/']
        # for link in links_to_scrape: # for real use
        for link in test_links:
            yield SeleniumRequest(url=link, callback=self.gather_information, wait_time=10)

    def gather_information(self, response):
        if isinstance(response, str):
            obj = BeautifulSoup(response, "html.parser")
        else:
            obj = BeautifulSoup(response.text, "html.parser")
        keyword_extraction_class = Keyword_Extraction_Class.KeywordExtraction()
        formatted_string = keyword_extraction_class.formate_input_text(obj.text)
        keywords = keyword_extraction_class.create_keywords(formatted_string)

        gather_information_class = Gather_Information_Class.GatherInformation()
        gather_information_class.get_years(obj.text)
        person_object.hobbies.extend(gather_information_class.compare_keywords_with_hobbies(keywords))
        person_object.locations.extend(gather_information_class.compare_keywords_with_locations(keywords))
        person_object.universities.extend(gather_information_class.compare_keywords_with_universities(keywords))
        person_object.occupation.extend(gather_information_class.compare_keywords_with_occupations(keywords))
        person_object.email.extend(gather_information_class.get_email(obj.body.text,person_object.first_name, person_object.second_name))

        print("Object" + person_object.first_name)
        print("Object" + person_object.second_name)
        print("Object" + person_object.place_of_residence)
        print("Object" + person_object.year_of_birth)
        print("Object" + person_object.estimated_year_of_birth)
        print("Object" + person_object.institution)
        print("Object", person_object.email)




# transfer information from user input
"""def transfer_information():
    person_input_information = create_search_link.enter_information()
    person_object.first_name = person_input_information.first_name
    person_object.second_name = person_input_information.second_name
    person_object.location = person_input_information.location
    person_object.institution = person_input_information.institution
    person_object.year_of_birth = person_input_information.year_of_birth
    person_object.estimated_year_of_birth = person_input_information.estimated_year_of_birth
"""

# Create Person object
#create_search_link = Create_Search_Link_Class.CreateSearchLink()
person_object = Person()

#transfer_information()



process = CrawlerProcess({
    "user-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"
})
process.crawl(QuotesSpider)
process.start()
