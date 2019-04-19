import requests
from bs4 import BeautifulSoup
import re
import csv

list = []

def get_names(html):

    names = html.find_all("a", attrs={"class": "searchCol1_Kunde_unbezahlt"})
    with open('ravensburg_institutionen.csv', 'a') as f:
        writer = csv.writer(f)
        for name in names:
            #print(list)
            if name.text not in list:
                print(name.text)
                writer.writerow([name.text])
                list.append(name.text)
    further_links = html.find_all("a", attrs={"href": re.compile("(https://www.firmenfinden.de/Content/MapSites/).*")})

    for link in further_links:
        if link.text == "vor":
            #print("VOOOOOOOR", link.text)
            req = session.get(link["href"], headers=headers)
            html = BeautifulSoup(req.text, "html.parser")
            get_names(html)
            return

link = "https://www.firmenfinden.de/Content/MapSites/MapResult.cshtml?Key=03030917&pagesize=100&optLtDs=1"

session = requests.Session()
headers = {"user-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

req = session.get(link, headers=headers)
html = BeautifulSoup(req.text, "html.parser")

names = html.find_all("a", attrs={"class":"searchCol1_Kunde_unbezahlt"})

with open('ravensburg_institutionen.csv', 'w') as f:
    writer = csv.writer(f)
    for name in names:
        if name.text not in list:
            print(name.text)
            writer.writerow([name.text])
            list.append(name.text)

further_links = html.find_all("a",attrs={"href":re.compile("(https://www.firmenfinden.de/Content/MapSites/).*")})
for link in further_links:
    print(link)
    if link.text == "vor":
        req = session.get(link["href"], headers=headers)
        html = BeautifulSoup(req.text, "html.parser")
        get_names(html)

