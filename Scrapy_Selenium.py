from scrapy_selenium import SeleniumRequest
import scrapy
from scrapy.crawler import CrawlerProcess
from shutil import which
from bs4 import BeautifulSoup
import Create_Search_Link_Class
import Keyword_Extraction_Class
import Gather_Information_Class
import Social_Media_Class
import Handle_Google_Results_Class
import csv
import re


class Person(object):
    def __init__(self):
        self.first_name = input("Vorname: ").replace(" ", "%22").lower()
        self.second_name = input("Nachname: ").replace(" ", "%22").lower()
        self.place_of_residence = input("Wohnort: ").replace(" ", "%22").lower()
        self.year_of_birth = input("Genaues Geburtsjahr: ").replace(" ", "%22")
        self.estimated_year_of_birth = input("Geschätztes Geburtsjahr: ").replace(" ", "%22")
        self.institution = input("Institution: ").replace(" ", "%22")
        self.instagram_name = input("Instagram Benutzername: ")
        self.facebook_name = input("Facebook Benutzername: ")
        self.twitter_name = input("Twitter Benutzername: ")
        self.input_email = input("E-Mail-Adresse: ")
        self.occupation = []
        self.hobbies = []
        self.universities = []
        self.founded_mails = []
        self.locations = []
        self.contacts_information = []


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
        self.person_object = Person()
        self.count = 0

    def start_requests(self):
        self.compare_place_of_residence_with_database()
        #For link-creation
        #TODO new Information should be used in google search
        #social_media = Social_Media_Class.SocialMedia()
        #self.transfer_information(social_media.handle_social_media(self.person_object))
        create_search_link = Create_Search_Link_Class.CreateSearchLink()
        search_url_list = create_search_link.get_search_links(self.person_object)
        print("URL-LIST: ", search_url_list)


        """search_url_list = ['https://www.google.com/search?q="Marco+Lang"+"Tettnang"+"1995"',
                'https://www.schwaebische.de/landkreis/bodenseekreis/tettnang_artikel,-junge-union-will-partty-bus-\
                verwirklichen-_arid,10701303.html']"""
        for url in search_url_list:
            print("Search for URL: ",url)
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)

    def parse(self, response):
        handle_google_results_class = Handle_Google_Results_Class.HandleGoogleResults()
        links_to_scrape_list = handle_google_results_class.handle_google_results(response)
        print(links_to_scrape_list)
        # For testing
        social_media = Social_Media_Class.SocialMedia()
        for link in links_to_scrape_list:
            test = re.compile(r'.*((instagram)|(twitter)|(linkedin)).*')
            if test.match(link):
                social_media.handle_social_media_url(link)
            else:
                yield SeleniumRequest(url=link, callback=self.gather_information, wait_time=10)

    def gather_information(self, response):
        print("IN GATHER INFORMATION", self.count)
        print(response.url)
        self.count = self.count +1

        if isinstance(response, str):
            obj = BeautifulSoup(response, "html.parser")
        else:
            try:
                obj = BeautifulSoup(response.text, "html.parser")
            except:
                return
        #Look for attributs like firstname, secondname and place_of_residence

        string = self.person_object.first_name+" "+self.person_object.second_name+" "
        print("User", string)
        if string in str(obj.text).lower():
            if self.person_object.place_of_residence in str(obj.text.lower()):
                print("ALLLLLLLLLES GEFUNDEN")

                keyword_extraction_class = Keyword_Extraction_Class.KeywordExtraction()
                formatted_string = keyword_extraction_class.formate_input_text(obj.text)
                keywords = keyword_extraction_class.create_keywords(formatted_string)

                gather_information_class = Gather_Information_Class.GatherInformation()
                gather_information_class.get_years(obj.text)
                self.person_object.hobbies.extend(gather_information_class.compare_keywords_with_hobbies(keywords))
                self.person_object.locations.extend(gather_information_class.compare_keywords_with_locations(keywords))
                self.person_object.universities.extend(gather_information_class.compare_keywords_with_universities(keywords))
                self.person_object.occupation.extend(gather_information_class.compare_keywords_with_occupations(keywords))
                self.person_object.founded_mails.extend(gather_information_class.get_email(obj.body.text, self.person_object.first_name, self.person_object.second_name))

                print("names", self.person_object.first_name)
                print("instiution",self.person_object.universities)
                print("locations",self.person_object.locations)

    def transfer_information(self, social_media_person):
        if self.person_object.first_name == "":
            self.person_object.first_name = social_media_person.first_name
        if self.person_object.second_name == "":
            self.person_object.second_name= social_media_person.second_name
        self.person_object.occupation = social_media_person.occupation
        self.person_object.locations = social_media_person.locations
        self.person_object.universities = social_media_person.universities
        self.person_object.contacts_information = social_media_person.contacts_information
        self.person_object.founded_mails = social_media_person.email
        self.person_object.hobbies = social_media_person.hobbies

    def compare_place_of_residence_with_database(self):
        database_word_list_location= []
        place_of_residence_in_database = False
        if self.person_object.place_of_residence is not "":
            with open('location.csv', 'r') as csvFile:
                # with open('hobbies.csv', 'r') as csvFile:
                csv_reader = csv.reader(csvFile)
                for row in csv_reader:
                    database_word_list_location.append(row[0].lower())
                for element in database_word_list_location:
                    # if element in word:
                    if element == self.person_object.place_of_residence:
                        place_of_residence_in_database = True
            csvFile.close()
            if not place_of_residence_in_database:
                with open("location.csv", "a")as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow([self.person_object.place_of_residence])
                csvFile.close()




# transfer information from user input


# Create Person object
# create_search_link = Create_Search_Link_Class.CreateSearchLink()
#person_object = Person()
# transfer_information()
process = CrawlerProcess({
    "user-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"
})
process.crawl(QuotesSpider)
process.start()
