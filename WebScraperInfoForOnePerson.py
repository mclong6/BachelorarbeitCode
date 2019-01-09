from bs4 import BeautifulSoup
import re
from selenium import webdriver
# Mechanize cannot execute javascript and send asynchronous requests, but Selenium can do it;If you want to scrap a
# static website, Mechanize is better(provides friendly apis and quickly);If you want to scrap any SPA(like AngularJS,
# ReactJS,VueJS) website, Selenium can help you;If you need to auto login, it depends the web page needs to execute JS
# or not.

username = "bachelorarbeit2@gmx.de"
password = "bachelorarbeit2"


class Person(object):
    def __init__(self, first_name, second_name, location, year_of_birth):
        self.first_name = first_name
        self.second_name = second_name
        self.location = location
        self.year_of_birth = year_of_birth


def get_person_information():
    first_name= input("Vorname: ")
    second_name = input("Nachname: ")
    location = input("Ort: ")
    year_of_birth = input("Geburtsjahr: ")

    person = Person(first_name, second_name, location, year_of_birth)
    print(person.year_of_birth)


def login_xing(username, password):
    url_german_companies = "https://www.xing.com/search/companies?advanced_form=true&nrs=1&" \
                           "section=companies&filters%5Bcountry%5D%5B%5D=2921044"
    browser = webdriver.Chrome('/home/marco/Downloads/chromedriver')
    browser.implicitly_wait(10)
    browser.implicitly_wait(10)
    browser.maximize_window()
    browser.get("https://login.xing.com/login")
    browser.find_element_by_name("login_form[username]").send_keys(username)
    browser.find_element_by_name("login_form[password]").send_keys(password)
    browser.find_element_by_name("button").click()


get_person_information()
#ogin_xing(username, password)