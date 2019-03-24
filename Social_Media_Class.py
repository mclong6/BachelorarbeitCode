from bs4 import BeautifulSoup
import re
import time
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
        time.sleep(1)

    def search_instagram(self,instagram_name):
        print("in search_instagram")
        search_url = "https://www.instagram.com/" + instagram_name + "/"
        self.browser.get(search_url)
        html_of_search = self.browser.page_source
        html = BeautifulSoup(html_of_search, "html.parser")

        """person_soup = html.find("div", attrs={"class": "-vDIg"})
               print(person_soup.prettify())

               search = "https://www.google.com/search?q=site%3Ainstagram.com+%27" + instagram_name + "%27+-site%3Ainstagram.com%2F" + \
                        instagram_name + "&oq=site%3Ainstagram.com+%27" + \
                        instagram_name + "%27+-site%3Ainstagram.com%2F" + instagram_name
               self.browser.get(search)"""

        return html_of_search


"""test = SocialMedia()
test.login_to_any_page("https://www.instagram.com/accounts/login/?next=%2Fbachelor_arbeit2%2F&source=desktop_nav")
test.search_instagram("lamarcong")"""