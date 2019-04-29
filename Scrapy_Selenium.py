from scrapy_selenium import SeleniumRequest
import scrapy
from scrapy.crawler import CrawlerProcess
from shutil import which
from bs4 import BeautifulSoup
import csv
import re
import Create_Search_Link_Class
import Keyword_Extraction_Class
import Gather_Information_Class
import Social_Media_Class
import Handle_Google_Results_Class
import Create_Phishing_Mail_Class
import Choose_Information_Class
import time


# person object, in this object all information about the searched person is stored
class Person(object):
    def __init__(self):
        time.sleep(1)
        print("\nZugelassene Eingaben sind:")
        print("- Geschlecht, Vorname, Nachname, Wohnort/Standort;")
        print("- Geschlecht, Vorname, Nachname, Geburtsjahr;")
        print("- Geschlecht, Social-Media-Benutzername;")
        print("- Geschlecht, E-Mail-Adresse;\n")
        self.sex = input("Geschlecht m/w: ").replace(" ", "%22").lower()
        self.first_name = input("Vorname: ").replace(" ", "%22").lower()
        self.second_name = input("Nachname: ").replace(" ", "%22").lower()
        self.place_of_residence = input("Wohnort/Standort: ").replace(" ", "%22").lower()
        self.year_of_birth = input("Genaues Geburtsjahr: ").replace(" ", "%22")
        self.institution = input("Institution: ")
        self.instagram_name = input("Instagram Benutzername: ")
        #self.facebook_name = input("Facebook Benutzername: ")
        self.twitter_name = input("Twitter Benutzername: ")
        self.input_email = input("E-Mail-Adresse: ")
        self.occupation = []
        self.hobbies = []
        self.universities = []
        self.institutions_found = []
        self.mails_found = []
        self.locations = []
        self.contacts_information = []
        self.visited_links = []


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
        self.header = {"user-Agent":"Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu "
                                    "Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                       "accept-encoding": "gzip, deflate, br"}

        self.instagram_key = 1
        self.facebook_key = 2
        self.twitter_key = 3
        self.linkedin_key = 4
        self.xing_key = 5
        global person_object
        person_object = Person()
        self.count = 0
        self.counter = 1
        self.length_for_counter = 0
        self.social_media = Social_Media_Class.SocialMedia()
        self.instagram_regex = re.compile(r'.*(instagram).*')
        self.twitter_regex = re.compile(r'.*(twitter).*')
        self.linkedin_regex = re.compile(r'.*(linkedin).*')
        self.xing_regex = re.compile(r'.*(xing).*')

    def start_requests(self):
        if person_object.sex == "":
            print("Geben Sie bitte das Geschlecht der Zielperson an.")
            self.social_media.close_browser()
        else:
            self.compare_place_of_residence_with_database()
            self.transfer_information(self.social_media.handle_social_media(person_object))
            create_search_link = Create_Search_Link_Class.CreateSearchLink()
            search_url_list = create_search_link.get_search_links(person_object)
            print("URL-Liste: ", search_url_list)

            for url in search_url_list:
                yield SeleniumRequest(url=url, callback=self.parse, wait_time=5)

    # handle results from google search
    def parse(self, response):
        handle_google_results_class = Handle_Google_Results_Class.HandleGoogleResults()
        links_to_scrape_list = handle_google_results_class.handle_google_results(response)
        print(links_to_scrape_list)
        self.length_for_counter = len(links_to_scrape_list)
        for link in links_to_scrape_list:
            if link not in person_object.visited_links:
                if self.instagram_regex.match(link):
                    self.social_media.handle_social_media_url(link, self.instagram_key)
                elif self.twitter_regex.match(link):
                    self.social_media.handle_social_media_url(link, self.twitter_key)
                elif self.linkedin_regex.match(link):
                    self.social_media.handle_social_media_url(link, self.linkedin_key)
                elif self.xing_regex.match(link):
                    self.social_media.handle_social_media_url(link, self.xing_key)
                else:
                    yield SeleniumRequest(url=link, headers=self.header, callback=self.gather_information, wait_time=10)
                    person_object.visited_links.append(link)

    def gather_information(self, response):
        self.counter += 1
        if isinstance(response, str):
            obj = BeautifulSoup(response, "html.parser")
        else:
            try:
                obj = BeautifulSoup(response.text, "html.parser")
            except:
                return
        # check which attributes are known
        if person_object.first_name and person_object.second_name:
            person_name_string = person_object.first_name+" "+person_object.second_name
            if person_name_string in str(obj.text).lower() or person_object.input_email:
                if person_object.place_of_residence:
                    self.get_data(person_object.place_of_residence, obj)
                elif person_object.year_of_birth:
                    self.get_data(person_object.year_of_birth, obj)
                elif person_object.institution:
                    self.get_data(person_object.institution, obj)
        elif person_object.input_email:
            self.get_data(person_object.input_email, obj)

    def get_data(self, string, obj):
        # filter out websites that do not meet any of the following criteria
        if string in str(obj.text).lower():
            keyword_extraction_class = Keyword_Extraction_Class.KeywordExtraction()
            formatted_string = keyword_extraction_class.formate_input_text(obj.text)
            keywords = keyword_extraction_class.create_keywords(formatted_string)

            gather_information_class = Gather_Information_Class.GatherInformation()
            if not person_object.year_of_birth:
                year = gather_information_class.get_years(keywords)
                if year != -1:
                    person_object.year_of_birth = year

            current_hobbies = gather_information_class.compare_keywords_with_hobbies(keywords)
            if current_hobbies != -1:
                person_object.hobbies.append(current_hobbies)
            person_object.locations.append(gather_information_class.compare_keywords_with_locations(keywords))

            current_institution = gather_information_class.compare_keywords_with_institutions(obj.text)
            if current_institution != -1:
                person_object.institutions_found.append(current_institution)

            current_occupations = gather_information_class.compare_keywords_with_occupations(keywords)
            if current_occupations != -1:
                person_object.occupation.append(current_occupations)

            current_mails = gather_information_class.get_email(obj.text, person_object.first_name, person_object.second_name)
            if current_mails != -1:
                for mail in current_mails:
                    if mail not in person_object.mails_found:
                        person_object.mails_found.append(mail)

    # transfer the data found in the social media class to the person object.
    def transfer_information(self, social_media_person):
        if person_object.first_name == "":
            person_object.first_name = social_media_person.first_name
        if person_object.second_name == "":
            person_object.second_name= social_media_person.second_name
        person_object.occupation = social_media_person.occupation
        person_object.locations = social_media_person.locations
        person_object.institutions_found = social_media_person.institutions_found
        person_object.contacts_information = social_media_person.contacts_information
        person_object.mails_found = social_media_person.email
        person_object.hobbies = social_media_person.hobbies
        person_object.mails_found = social_media_person.mails_found
        person_object.visited_links = social_media_person.visited_links

    # add place of residence to database, if it is not included
    def compare_place_of_residence_with_database(self):
        database_word_list_location= []
        place_of_residence_in_database = False
        if person_object.place_of_residence is not "":
            with open('location.csv', 'r') as csvFile:
                # with open('hobbies.csv', 'r') as csvFile:
                csv_reader = csv.reader(csvFile)
                for row in csv_reader:
                    database_word_list_location.append(row[0].lower())
                for element in database_word_list_location:
                    # if element in word:
                    if element == person_object.place_of_residence:
                        place_of_residence_in_database = True
            csvFile.close()
            if not place_of_residence_in_database:
                with open("location.csv", "a")as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow([person_object.place_of_residence])
                csvFile.close()

print("\n--------OSINT-Anwednung einer ausgwählten Person--------\n")

process = CrawlerProcess({
    "user-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"
})
process.crawl(QuotesSpider)
process.start()
key_institution = 1
key_other = 2
choose_information_class = Choose_Information_Class.ChooseInformation()
choose_information_class.get_highest_score(person_object.locations, key_other)
person_object.locations = choose_information_class.get_highest_score(person_object.locations,key_other)
person_object.occupation = choose_information_class.get_highest_score(person_object.occupation,key_other)
person_object.hobbies = choose_information_class.get_highest_score(person_object.hobbies,key_other)
person_object.institutions_found = choose_information_class.get_highest_score(person_object.institutions_found, key_institution)

print("\nPersonenprofil:\n")
print("Vorname: ", person_object.first_name)
print("Nachname: ", person_object.second_name)
print("Wohnort/Standort:", person_object.place_of_residence)
print("Geburtsjahr:", person_object.year_of_birth)
print("Location:", person_object.locations )
print("Occupations:", person_object.occupation)
print("Hobbies:", person_object.hobbies)
print("Institution gefunden:", person_object.institutions_found)
print("E-Mail: ", person_object.mails_found)
print("Kontaktinformation: ", person_object.contacts_information)
print("Links visited: ",person_object.visited_links)

create_phishing_mail_class = Create_Phishing_Mail_Class.CreatePhishingMail()
create_phishing_mail_class.create_phishing_mail(person_object)