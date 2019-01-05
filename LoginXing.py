import requests
from bs4 import BeautifulSoup
headers = {"user-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

login_data = {
    'utf8': '✓',
    'logged_out_sid': '25c4698c7ba88725e85c333790ced49f',
    'locale': 'de',
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

    req = session.get(url, headers= headers)
    soup = BeautifulSoup(req.content,"html5lib")
    #login_data['login_form[dest_url]'] = soup.find("input", attrs={"name": "login_form[dest_url]"})["value"]

    r = session.post(url,data=login_data,headers=headers)
    print(req.content)