from bs4 import BeautifulSoup
import re
from selenium import webdriver
# Mechanize cannot execute javascript and send asynchronous requests, but Selenium can do it;If you want to scrap a
# static website, Mechanize is better(provides friendly apis and quickly);If you want to scrap any SPA(like AngularJS,
# ReactJS,VueJS) website, Selenium can help you;If you need to auto login, it depends the web page needs to execute JS
# or not.

url = "/profile/Wolfgang_Zeilmann"
browser = webdriver.Chrome('/home/marco/Downloads/chromedriver')
browser.get("https://login.xing.com/login")
browser.implicitly_wait(10)
browser.find_element_by_name("login_form[username]").send_keys("bachelorarbeit2@gmx.de")
browser.find_element_by_name("login_form[password]").send_keys("bachelorarbeit2")
browser.find_element_by_name("button").click()

browser.implicitly_wait(10)
browser.maximize_window()
browser.find_element_by_name("keywords").send_keys("Wolfgang Zeilmann\n")
html_of_search = browser.page_source
soup = BeautifulSoup(html_of_search, "html.parser")

print(soup.prettify())

all_links = soup.find_all("a", attrs={'href': re.compile("^(/profile/).*_.*/.*")})
for link in all_links:
    print('------------------------------------------------------')
    print(link.attrs['href'])
    browser.get('https://www.xing.com'+link.attrs['href'])
