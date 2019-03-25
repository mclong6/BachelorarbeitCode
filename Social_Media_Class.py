from bs4 import BeautifulSoup
import re
import time
import Keyword_Extraction_Class
import Gather_Information_Class
from selenium.webdriver.common.by import By
from selenium import webdriver
import Handle_Google_Results_Class
from nltk import word_tokenize
# Mechanize cannot execute javascript and send asynchronous requests, but Selenium can do it;If you want to scrap a
# static website, Mechanize is better(provides friendly apis and quickly);If you want to scrap any SPA(like AngularJS,
# ReactJS,VueJS) website, Selenium can help you;If you need to auto login, it depends the web page needs to execute JS
# or not.
class Person(object):
    def __init__(self):
        self.first_name = ""
        self.second_name = ""
        self.place_of_residence = ""
        self.year_of_birth = ""
        self.estimated_year_of_birth = ""
        self.institution = ""
        self.instagram_name = ""
        # self.facebook_name = ""
        self.twitter_name = ""
        self.occupation = []
        self.hobbies = []
        self.universities = []
        self.email = []
        self.locations = []
        self.contacts_information = []

class SocialMedia:
    def __init__(self):
        self.username = "bachelorarbeit2@gmx.de"
        self.password = "bachelorarbeit2"
        self.instagram_key = 1
        self.facebook_key = 2
        self.twitter_key = 3
        self.facebook_login_page = "https://www.facebook.com/login.php"
        self.instagram_login_page = "https://www.instagram.com/accounts/login/?next=%2Fbachelor_arbeit2%2F&source=desktop_nav"
        self.xing_login_page = "https://login.xing.com/login"
        self.linkedin_login_page = "https://www.linkedin.com/uas/login"
        self.twitter_login_page = "https://twitter.com/login"
        self.browser = webdriver.Chrome('/home/marco/Downloads/chromedriver')
        self.browser.implicitly_wait(10)
        self.url = ""
        self.contacts_of_victim = []
        self.instagram_login = False
        self.facebook_login = False
        self.twitter_login = False
        self.person_object = Person()

    def login_to_any_page(self, key):
        if key == self.facebook_key:
            self.url = self.facebook_login_page
        elif key == self.instagram_key:
            self.url = self.instagram_login_page
        elif key == self.twitter_key:
            print("login Twiittttter")
            self.url = self.twitter_login_page

        self.browser.maximize_window()
        self.browser.get(self.url)
        time.sleep(1)
        html_of_search = self.browser.page_source
        html = BeautifulSoup(html_of_search, "html.parser")
        input_username = html.find("input", attrs={'type': re.compile("^(text)|(email)")})
        input_password = html.find("input", {"type":"password"})
        id_username = input_username.attrs["id"]
        id_password = input_password.attrs["id"]
        time.sleep(1)
        self.browser.find_element_by_id(id_username).send_keys(self.username)
        self.browser.find_element_by_id(id_password).send_keys(self.password+"\n")
        time.sleep(2)

    def handle_social_media(self, person):
        self.person_object = person
        print(self.person_object.first_name,self.person_object.second_name,self.person_object.place_of_residence)
        print("handle_social_media()")
        if self.person_object.instagram_name:
            self.login_to_any_page(self.instagram_key)
            self.instagram_login = True
            self.handle_instagram()
            self.search_trough_contacts(self.instagram_key)
        if self.person_object.twitter_name:
            self.login_to_any_page(self.twitter_key)
            self.twitter_login = True
            self.handle_twitter()

        """if self.person_object.facebook_name:
            self.login_to_any_page(self.facebook_key)

        """

        return self.person_object

    def handle_twitter(self):
        print("handle_twitter")
        search_url_list = self.create_search_links(self.twitter_key)
        print(search_url_list[0])

    def handle_instagram(self):
        print("handle_instagram()")
        search_url_list = self.create_search_links(self.instagram_key)
        url_to_profil = search_url_list[0]
        url_to_further_information = search_url_list[1]

        # handle profile site
        self.handle_instagram_url(url_to_profil)
        # Just for testing
        # self.search_trough_contacts(self.instagram_key, person_object)

        # handle_further_information
        self.browser.get(url_to_further_information)
        html_of_search = self.browser.page_source
        handle_google_results_class = Handle_Google_Results_Class.HandleGoogleResults()
        links_to_scrape = handle_google_results_class.handle_google_results(html_of_search)
        print(links_to_scrape)
        for link in links_to_scrape:
            self.handle_instagram_url(link)

    def handle_instagram_url(self, url):
        self.browser.get(url)
        html_of_search = self.browser.page_source
        html_soup = BeautifulSoup(html_of_search, "html.parser")
        self.gather_information(html_soup.text)

    def gather_information(self, text, ):
        keyword_extraction_class = Keyword_Extraction_Class.KeywordExtraction()
        formatted_text = keyword_extraction_class.formate_input_text(text)
        keywords = keyword_extraction_class.create_keywords(formatted_text)
        gather_information_class = Gather_Information_Class.GatherInformation()
        self.person_object.contacts_information.extend(gather_information_class.compare_keywords_with_hobbies(keywords))
        self.person_object.contacts_information.extend(gather_information_class.compare_keywords_with_locations(keywords))
        self.person_object.contacts_information.extend(gather_information_class.compare_keywords_with_universities(keywords))
        self.person_object.contacts_information.extend(gather_information_class.compare_keywords_with_occupations(keywords))

    def search_trough_contacts(self, key):
        if key == self.instagram_key:
            try:
                while 1:
                    html_of_search = self.browser.page_source
                    html = BeautifulSoup(html_of_search, "html.parser")
                    for div in html.find_all("div", attrs={"class":"_41KYi LQtnO"}):
                            for a_tag in div.find_all("a", attrs={'href': re.compile("/[a-z0-9.\-]/*")}):
                                #print(a_tag.attrs["href"])
                                if a_tag.attrs["href"] not in self.contacts_of_victim:
                                    self.contacts_of_victim.append(a_tag.attrs["href"])
                                    print(self.contacts_of_victim)
                    self.browser.find_element_by_xpath("//*[@class='Szr5J  _6CZji']").click()
            except Exception as e:
                print("no more links")
                print(e)

            for contact_link in self.contacts_of_victim:
                print(contact_link)
                url = "https://www.instagram.com" + contact_link
                self.browser.get(url)
                html_of_search = self.browser.page_source
                html = BeautifulSoup(html_of_search, "html.parser")
                test = html.find_all("section")
                print(test[1].text)

                """url = "https://www.instagram.com/michi0595"
                self.browser.get(url)
                #time.sleep(2)
                html_of_search = self.browser.page_source
                html = BeautifulSoup(html_of_search, "html.parser")
                test = html.find_all("section")
                print(test[1].text)"""

                keyword_extraction_class = Keyword_Extraction_Class.KeywordExtraction()
                formatted_text = keyword_extraction_class.formate_input_text(test[1].text)
                keywords = keyword_extraction_class.create_keywords(formatted_text)
                gather_information_class = Gather_Information_Class.GatherInformation()
                self.person_object.contacts_information.extend(gather_information_class.compare_keywords_with_hobbies(keywords))
                self.person_object.contacts_information.extend(gather_information_class.compare_keywords_with_locations(keywords))
                self.person_object.contacts_information.extend(gather_information_class.compare_keywords_with_universities(keywords))
                self.person_object.contacts_information.extend(gather_information_class.compare_keywords_with_occupations(keywords))

        print(self.person_object.contacts_information)
        #return person_object

    def create_search_links(self, key):
        search_url_list = []
        if key == self.instagram_key:
            search_url_list.append("https://www.instagram.com/" + self.person_object.instagram_name + "/")
            search_url_list.append("https://www.google.com/search?q=site%3Ainstagram.com+%27" + self.person_object.instagram_name +
                                        "%27+-site%3Ainstagram.com%2F" + self.person_object.instagram_name + "&oq=site%3Ainstagram.com+%27" +
                                        self.person_object.instagram_name + "%27+-site%3Ainstagram.com%2F" + self.person_object.instagram_name)
        elif key == self.twitter_key:
            search_url_list = "https://twitter.com/search?f=users&q="+ self.person_object.twitter_name

        return search_url_list

"""class Person(object):
    def __init__(self):
        self.first_name = "marco"
        self.second_name = ""
        self.place_of_residence = ""
        self.year_of_birth = ""
        self.estimated_year_of_birth = ""
        self.institution = ""
        self.instagram_name = "michi0595"
        # self.facebook_name = input("Facebook Benutzername: ")
        # self.twitter_name = input("Twitter Benutzername")
        self.occupation = []
        self.hobbies = []
        self.universities = []
        self.email = []
        self.locations = []
        self.contacts_information = []
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
        self.estimated_year_of_birth = 

person = Person()
test = SocialMedia()
test.login_to_any_page(1)
test.handle_instagram(person)
#test.search_trough_contacts(1, person)"""

