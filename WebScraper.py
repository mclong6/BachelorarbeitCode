from bs4 import BeautifulSoup
from urllib.error import HTTPError
import requests
import re

url = "https://www.fupa.net"
# A set is an unordered collection of items.
# Every element is unique (no duplicates) and must be immutable (which cannot be changed).
# However, the set itself is mutable. We can add or remove items from it.
# Sets can be used to perform mathematical set operations like union, intersection, symmetric difference etc.
linkAlreadyVisitedCollection = set()
linksToPlayerCollection = set()

# WICHTIG
# Header-Umschreiben sonst Fehler 451
# Standard-Http-Header von Python wird oft gesperrt um web scraping zu verhindern
# Standard Python Header:
# Accept-Encoding:   identity
# User-Agent:        Python-urllib/3.7
session = requests.Session()
headers = {"user-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
linksToPlayerFile = open("linksToPlayerFile.txt", "w")

noDepth = 0
firstDepth = 1
secondDepth = 2
thirdDepth = 3
fourthDepth = 4


def get_new_html(link):
    # req = session.get(url+"/club/jsg-union-dessau/calender/2030-03/club/sportunion-wacker-sued/calender/2018-10",
    # headers=headers)
    # for testing
    req = ""
    try:
        if re.match(r"https://.*", link) is not None:
            req = session.get(link, headers=headers)
        else:
            req = session.get(url + link, headers=headers)

    except HTTPError as e:
        print(e)
    html = BeautifulSoup(req.text, "html.parser")
    return html


def search_breadth(depth, html):
    if html is None or len(html) == 0:
        print("!!   NO HTML    !!")
    else:
        for a_tag in html.find_all("a", attrs={'href': re.compile("^.*")}):
            # To have only one format of links
            if re.match(r"https://www.fupa.net.*", a_tag.attrs['href']) is None:
                formatted_link = "https://www.fupa.net" + a_tag.attrs['href']
            else:
                formatted_link = a_tag.attrs['href']
            # check if link was already visited
            if formatted_link not in linkAlreadyVisitedCollection and formatted_link not in linksToPlayerCollection:
                if depth == noDepth:
                    if 'id' in a_tag.attrs:
                        if re.match(r"(navi_link_)[0-9]{1,3}", a_tag.attrs['id']) is not None:
                            # print(formatted_link)
                            linkAlreadyVisitedCollection.add(formatted_link)
                            search_breadth(depth + 1, get_new_html(formatted_link))
                elif depth == firstDepth:
                    if 'data-level' in a_tag.attrs:
                        if a_tag.attrs['data-level'] == "3":
                            search_breadth(depth + 1, get_new_html(formatted_link))
                            print(a_tag)
                elif depth == secondDepth:
                    if re.match(r".*(/liga/).*", formatted_link) is not None:
                        # print(formatted_link)
                        linkAlreadyVisitedCollection.add(formatted_link)
                        search_breadth(depth + 1, get_new_html(formatted_link))
                elif depth == thirdDepth:
                    if re.match(r".*(/club/).*", formatted_link) is not None:
                        linkAlreadyVisitedCollection.add(formatted_link)
                        search_breadth(depth + 1, get_new_html(formatted_link))
                elif depth == fourthDepth:
                    if re.match(r"(https://www.fupa.net/spieler/)[a-z+\-]*[0-9]{5,6}", formatted_link) is not None:
                        linksToPlayerCollection.add(formatted_link)
                        linksToPlayerFile.write(formatted_link + "\n")
                        linkAlreadyVisitedCollection.add(formatted_link)
                        print("Player found and added to the list")
                else:
                    print("!!   Depth is to big  !! Depth: ", depth)


search_breadth(noDepth, get_new_html(""))
# search_breadth(fourthDepth, get_new_html("https://www.fupa.net/club/tsv-tettnang/team/m1"))
