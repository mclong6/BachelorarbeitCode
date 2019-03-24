from bs4 import BeautifulSoup
import re
import time
import Keyword_Extraction_Class
import Gather_Information_Class
from selenium.webdriver.common.by import By
from selenium import webdriver
from nltk import word_tokenize
# Mechanize cannot execute javascript and send asynchronous requests, but Selenium can do it;If you want to scrap a
# static website, Mechanize is better(provides friendly apis and quickly);If you want to scrap any SPA(like AngularJS,
# ReactJS,VueJS) website, Selenium can help you;If you need to auto login, it depends the web page needs to execute JS
# or not.


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
        self.search_url_list = []
        self.contacts_of_victim = []

    def login_to_any_page(self, key):
        if key == self.facebook_key:
            self.url = self.facebook_login_page
        elif key == self.instagram_key:
            self.url = self.instagram_login_page
        elif key == self.twitter_key:
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

    def handle_instagram(self,person_object):
        print("handle_instagram()")
        self.create_search_links(person_object.instagram_name)

        for url in self.search_url_list:
            self.browser.get("https://www.instagram.com/michi0595/")
            time.sleep(2)
            html_of_search = self.browser.page_source
            html = BeautifulSoup(html_of_search, "html.parser")
            print(url)
            try:
                while 1:
                    #time.sleep(1.5)
                    html_of_search = self.browser.page_source
                    html = BeautifulSoup(html_of_search, "html.parser")
                    for div in html.find_all("div", attrs={"class":"_41KYi LQtnO"}):
                            for a_tag in div.find_all("a", attrs={'href': re.compile("/[a-z0-9.\-]/*")}):
                                #print(a_tag.attrs["href"])
                                if a_tag.attrs["href"] not in self.contacts_of_victim:
                                    self.contacts_of_victim.append(a_tag.attrs["href"])
                                    print(self.contacts_of_victim)
                    self.browser.find_element_by_xpath("//*[@class='Szr5J  _6CZji']").click()
                        #self.browser.find_element_by_xpath("//*[@class='Szr5J  _6CZji']").click()

            except:
                print("no more links")
            self.search_trough_contacts(self.instagram_key, person_object)

    def search_trough_contacts(self, key, person_object):
        if key == self.instagram_key:
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
                person_object.hobbies.extend(gather_information_class.compare_keywords_with_hobbies(keywords))
                person_object.locations.extend(gather_information_class.compare_keywords_with_locations(keywords))
                person_object.universities.extend(gather_information_class.compare_keywords_with_universities(keywords))
                person_object.occupation.extend(gather_information_class.compare_keywords_with_occupations(keywords))

        #return person_object

    def create_search_links(self,instagram_name):
        self.search_url_list.append("https://www.instagram.com/" + instagram_name + "/")
        """self.search_url_list.append("https://www.google.com/search?q=site%3Ainstagram.com+%27" + instagram_name +
                                    "%27+-site%3Ainstagram.com%2F" + instagram_name + "&oq=site%3Ainstagram.com+%27" +
                                    instagram_name + "%27+-site%3Ainstagram.com%2F" + instagram_name)"""

class Person(object):
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

person = Person()
test = SocialMedia()
test.login_to_any_page(1)
test.handle_instagram(person)
#test.search_trough_contacts(1, person)
