import requests

import time
from bs4 import BeautifulSoup
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

login_data = {
    'utf8': '✓',
    'locale': 'de',
    'logged_out_sid': 'a9717179796b59827ddee4121d4ca07c',
    'login_form[dest_url]': '/',
    'login_form[force_dest]': '0',
    'login_form[section]': 'core',
    'login_form[token_param]': 'auth_token',
    'login_form[username]': 'bachelorarbeit2@gmx.de',
    'login_form[password]': 'bachelorarbeit2',
    'login_form[perm]': '0',
    'login_form[perm]': '1'
}

with requests.Session() as session:
    url = 'https://login.xing.com/login'
    USERNAME = 'bachelorarbeit2@gmx.de'
    PASSWORD = 'bachelorarbeit2'

    session.get(url)
    login_request = session.post(url,data=login_data,headers=headers)
    print(session.cookies)
    #print(login_request.text)
    page = session.get('https://www.xing.com/profile/FriedrichKlaus_Petzak/cv?sc_o=da980_e', headers=headers)
    print(session.cookies)
    print('------------------------------------------------------------------------------------')
    #print(page.text)

    #req1 = session.get('https://www.xing.com/profile/Wolfgang_Zeilmann/cv?sc_o=da980_e', headers=headers)
    #soup1 = BeautifulSoup(req1.text, "html.parser")

   # req = session.get(url, headers=headers)
    #soup = BeautifulSoup(req.content, "html5lib")
    #login_data["authenticity_token:"] = soup.find("input", attrs={"name": "authenticity_token"})["value"]

    #req = session.post(url, login_data, headers=headers)
   # print(req.url)
   # time.sleep(20)
   # print(req.url)
   # #print(session.cookies.get_dict())
   # print('----------------------------------')
   # s = session.get('https://www.xing.com/app/startpage')
   # print(s.url)


