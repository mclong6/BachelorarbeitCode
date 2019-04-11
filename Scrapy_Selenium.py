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
import Create_Phishing_Mail_Class
import csv
import re


class Person(object):
    def __init__(self):
        self.first_name = input("Vorname: ").replace(" ", "%22").lower()
        self.second_name = input("Nachname: ").replace(" ", "%22").lower()
        self.place_of_residence = input("Wohnort: ").replace(" ", "%22").lower()
        self.year_of_birth = input("Genaues Geburtsjahr: ").replace(" ", "%22")
        self.estimated_year_of_birth = input("Geschätztes Geburtsjahr: ").replace(" ", "%22")
        self.institution = input("Institution: ")
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
        self.header = {"user-Agent":"Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu "
                                    "Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                       "accept-encoding": "gzip, deflate, br"}

        self.instagram_key = 1
        self.facebook_key = 2
        self.twitter_key = 3
        self.person_object = Person()
        self.count = 0
        self.counter = 1
        self.length_for_counter = 0

    def start_requests(self):
        self.compare_place_of_residence_with_database()
        #For link-creation
        #TODO new Information should be used in google search
        #social_media = Social_Media_Class.SocialMedia()
        #self.transfer_information(social_media.handle_social_media(self.person_object))
        create_search_link = Create_Search_Link_Class.CreateSearchLink()
        search_url_list = create_search_link.get_search_links(self.person_object)
        print("URL-LIST: ", search_url_list)

        for url in search_url_list:
            print("Search for URL: ",url)
            yield SeleniumRequest(url=url,callback=self.parse, wait_time=10)

        print("IN IF COUNTER")
        print("Vorname: ", self.person_object.first_name)
        print("Nachname: ", self.person_object.second_name)
        print("Wohnort:", self.person_object.place_of_residence)
        print("Geburtsjahr:", self.person_object.year_of_birth)
        print("Locations:", self.get_most_frequencies1(self.person_object.locations))
        print("Occupations:", self.get_most_frequencies1(self.person_object.occupation))
        print("Hobbies:", self.get_most_frequencies1(self.person_object.hobbies))
        print("Institution:", self.person_object.institution)
        print("E-Mail: ", self.person_object.founded_mails)
        create_phishing_mail_class = Create_Phishing_Mail_Class.CreatePhishingMail()

        create_phishing_mail_class.create_phishing_mail(self.person_object)

    def parse(self, response):
        handle_google_results_class = Handle_Google_Results_Class.HandleGoogleResults()
        links_to_scrape_list = handle_google_results_class.handle_google_results(response)
        print(links_to_scrape_list)
        # For testing
        social_media = Social_Media_Class.SocialMedia()
        self.length_for_counter = len(links_to_scrape_list)
        for link in links_to_scrape_list:
            test = re.compile(r'.*((instagram)|(twitter)|(linkedin)).*')
            if test.match(link):
                social_media.handle_social_media_url(link)
            else:
                yield SeleniumRequest(url=link, headers=self.header, callback=self.gather_information, wait_time=10)

    def gather_information(self, response):
        self.counter += 1
        if isinstance(response, str):
            obj = BeautifulSoup(response, "html.parser")
        else:
            try:
                obj = BeautifulSoup(response.text, "html.parser")
            except:
                return
        #Look for attributs
        if self.person_object.first_name and self.person_object.second_name:
            person_name_string = self.person_object.first_name+" "+self.person_object.second_name
            if person_name_string in str(obj.text).lower() or self.person_object.input_email:
                if self.person_object.place_of_residence:
                    self.get_data(self.person_object.place_of_residence, obj)
                elif self.person_object.year_of_birth:
                    self.get_data(self.person_object.year_of_birth, obj)
                elif self.person_object.institution:
                    self.get_data(self.person_object.institution, obj)
        elif self.person_object.input_email:
            self.get_data(self.person_object.input_email, obj)
        print(self.counter)
        print(self.length_for_counter)
        if self.counter == self.length_for_counter:
           print("in if")


    def get_most_frequencies(self,list):
        print("Final List",list)
        counter = 0
        element_with_most_frequency = ""
        for i in list:
            current_frequency = list.count(i)
            if (current_frequency > counter):
                counter = current_frequency
                element_with_most_frequency = i
        return element_with_most_frequency

    def get_data(self, string, obj):
        #check for the correct website
        if string in str(obj.text).lower():
            keyword_extraction_class = Keyword_Extraction_Class.KeywordExtraction()
            formatted_string = keyword_extraction_class.formate_input_text(obj.text)
            keywords = keyword_extraction_class.create_keywords(formatted_string)

            gather_information_class = Gather_Information_Class.GatherInformation()
            if not self.person_object.year_of_birth:
                year = gather_information_class.get_years(keywords)
                if year != -1:
                    self.person_object.year_of_birth = year
            current_hobbies = gather_information_class.compare_keywords_with_hobbies(keywords)
            if current_hobbies != -1:
                self.person_object.hobbies.append(current_hobbies)
            self.person_object.locations.append(gather_information_class.compare_keywords_with_locations(keywords))
            self.person_object.universities.extend(gather_information_class.compare_keywords_with_universities(keywords))
            current_occupations = gather_information_class.compare_keywords_with_occupations(keywords)
            if current_occupations != -1:
                self.person_object.occupation.append(current_occupations)
            self.person_object.founded_mails.extend(gather_information_class.get_email(obj.text, self.person_object.first_name, self.person_object.second_name))

    def get_most_frequencies1(self,list):
        list3 = []

        for i in range(0,len(list)):
            list2 = []
            for k in range(0,len(list[i])):
                list1 = []
                frequency = list[i].count(list[i][k])
                score = frequency/len(list[i])
                list1.append(list[i][k])
                list1.append(score)
                #for l in range(0,len(list_with_counted_words)):
                   # print("IN FOR")
                if len(list2) == 0:
                    list2.append(list1)
                else:
                    in_list = True
                    for l in range(0,len(list2)):
                        if list1[0] in list2[l][0]:
                            in_list = False
                    if in_list:
                        list2.append(list1)
            list3.append(list2)
        print(list3)
        final_list = []
        for i in range(0,len(list3)):
            for k in range(0,len(list3[i])):
                if i < len(list3)-1:
                    for m in range(i+1,len(list3)):
                        for n in range(0,len(list3[m])):
                            if list3[i][k][0] == list3[m][n][0]:
                                test = []
                                print("SAME FOUND", list3[i][k][0])
                                list3[i][k][1] = list3[i][k][1] + list3[m][n][1]
                                #test.append(list3[i][k][0])
                                #test.append(score)
                                if list3[i][k] not in final_list:
                                    final_list.append(list3[i][k])
                            else:
                                if not list3[i][k] in final_list:
                                    final_list.append(list3[i][k])
                else:
                    if not list3[i][k] in final_list:
                        final_list.append(list3[i][k])
        print("final list",final_list)
        score = 0
        element_with_highest_score = ""
        for i in final_list:
            current_score = i[1]
            if (current_score > score):
                score = current_score
                element_with_highest_score = i[0]
        print("Element with highest score: ",element_with_highest_score, score)

        return element_with_highest_score

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
