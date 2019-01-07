from bs4 import BeautifulSoup
import re
from selenium import webdriver
# Mechanize cannot execute javascript and send asynchronous requests, but Selenium can do it;If you want to scrap a
# static website, Mechanize is better(provides friendly apis and quickly);If you want to scrap any SPA(like AngularJS,
# ReactJS,VueJS) website, Selenium can help you;If you need to auto login, it depends the web page needs to execute JS
# or not.

url_german_companies = "https://www.xing.com/search/companies?advanced_form=true&nrs=1&" \
      "section=companies&filters%5Bcountry%5D%5B%5D=2921044"
browser = webdriver.Chrome('/home/marco/Downloads/chromedriver')
browser.implicitly_wait(10)
browser.implicitly_wait(10)
browser.maximize_window()

page_links_list = []
companies_list = []

username = "bachelorarbeit2@gmx.de"
password = "bachelorarbeit2"


def login_xing(username, password):
    browser.get("https://login.xing.com/login")
    browser.find_element_by_name("login_form[username]").send_keys(username)
    browser.find_element_by_name("login_form[password]").send_keys(password)
    browser.find_element_by_name("button").click()


def open_link(url):
    browser.get(url)
    html_of_search = browser.page_source
    html = BeautifulSoup(html_of_search, "html.parser")
    return html


def get_companies_links(html):
    page_links = html.find_all("a", attrs={'href': re.compile("^(/search/companies).*")})

    for link in page_links:
        if not link.attrs["href"] in page_links_list:
            companies_list.append(link.attrs['href'])

    print(len(companies_list))
    companies_links = html.find_all("a", attrs={'href': re.compile("^(https://www.xing.com/companies/|"
                                                                   "https://www.xing.com/company/).*")})

    print('------------------------------------------------------')

    for link in companies_links:
        if not link.attrs["href"] in companies_list:
            companies_list.append(link.attrs['href'])

    print(companies_list)


login_xing(username,password)
get_companies_links(open_link(url_german_companies))
