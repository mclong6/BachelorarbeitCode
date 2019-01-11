from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
# Mechanize cannot execute javascript and send asynchronous requests, but Selenium can do it;If you want to scrap a
# static website, Mechanize is better(provides friendly apis and quickly);If you want to scrap any SPA(like AngularJS,
# ReactJS,VueJS) website, Selenium can help you;If you need to auto login, it depends the web page needs to execute JS
# or not.

username = "bachelorarbeit2@gmx.de"
password = "bachelorarbeit2"
facebook_login_page = "https://www.facebook.com/login.php"
instagram_login_page = "https://www.instagram.com/accounts/login"
xing_login_page = "https://login.xing.com/login"
linkedin_login_page = "https://www.linkedin.com/uas/login"


class Person(object):
    def __init__(self, first_name, second_name, location, year_of_birth, instagram_name, facebook_name, company):
        self.first_name = first_name
        self.second_name = second_name
        self.location = location
        self.year_of_birth = year_of_birth
        self.instagram_name = instagram_name
        self.facebook_name = facebook_name
        self.company = company


def get_person_information():
    first_name = input("Vorname: ")
    second_name = input("Nachname: ")
    location = input("Ort: ")
    year_of_birth = input("Geburtsjahr: ")
    instagram_name = input("Instagram-Name: ")
    facebook_name = input("Facebook-Name: ")
    company = input("Firma: ")
    person_object = Person(first_name, second_name, location, year_of_birth, "michi0595", facebook_name, company)

    if person_object.instagram_name is not "":
        print(person_object.instagram_name)
        login_to_any_page(instagram_login_page)


def login_to_any_page(url):
    browser = webdriver.Chrome('/home/marco/Downloads/chromedriver')
    browser.implicitly_wait(10)
    browser.maximize_window()
    browser.get(url)

    html_of_search = browser.page_source
    html = BeautifulSoup(html_of_search, "html.parser")

    input_username = html.find("input", attrs={'type': re.compile("^(text)|(email)")})
    input_password = html.find("input", {"type":"password"})

    browser.find_element_by_id(input_username.attrs["id"]).send_keys(username)
    browser.find_element_by_id(input_password.attrs["id"]).send_keys(password+"\n")
    time.sleep(3)
    html_startpage = browser.page_source
    html = BeautifulSoup(html_startpage, "html.parser")

    search_field = html.find("input", attrs={'type': re.compile("^(text)")})
    print(search_field)

get_person_information()
# login_to_any_page(facebook_login_page)

# ogin_xing(username, password)