from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import requests
import re
import Stack

url = "https://www.fupa.net"
# A set is an unordered collection of items.
# Every element is unique (no duplicates) and must be immutable (which cannot be changed).
# However, the set itself is mutable. We can add or remove items from it.
# Sets can be used to perform mathematical set operations like union, intersection, symmetric difference etc.
pages = set()
playerLinks = set()


linkList1 = []
counter = 0


# WICHTIG
# Header-Umschreiben sonst Fehler 451
# Standard-Http-Header von Python wird oft gesperrt um web scraping zu verhindern
# Standard Python Header:
# Accept-Encoding:   identity
# User-Agent:        Python-urllib/3.7
session = requests.Session()
headers = {"user-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

# file includes playerLinks
playersFile = open("playersFile.txt","w")
nodesFile = open("nodeFile.txt","w")

stack = Stack.Stack()


def startPage():
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    else:
        #BeautfulSoup is a library for pulling data out of HTML and XML files
        #Parser to provide idomatic ways of navigation, search,...
        bsObj = BeautifulSoup(html, "html.parser")

        #find() is searching for div with the class navi_box
        naviBox = bsObj.find("div", {"class": "navi_box"})

        #Find als a-tags of the div container with a for loop
        for links in naviBox.find_all("a"):
            #search for the link attributes for "href"
            if 'href' in links.attrs:
                linkList1.append(url + links.attrs['href'])

        for ausgabe in linkList1:
            print(ausgabe)


def secondPage():
    try:
        html = urlopen("https://www.xing.com/profile/Thomas_Zimmermann238")
    except HTTPError as e:
        print("!!!!HTTPERROR!!!!")
        print(html.text)
        print(e)
    except URLError as e:
        print("!!!!URLERROR!!!!")
        print(e)
    else:
        # print(html.text)
        bsObj = BeautifulSoup(html, "html.parser")
        # find() is searching for div with the class navi_box
        print(bsObj.find_all("a"))


def getLinks(pageURL):
    # global variable use the global variable from the beginning
    global pages
    # req = session.get("https://www.fupa.net/club/sv-elversberg/team/m2", headers=headers) #for testing
    req = session.get(url + pageURL, headers=headers)
    bsObj = BeautifulSoup(req.text, "html.parser")

    # re = regular expression
    # re.compile compile to a regular expression object
    for link in bsObj.find_all("a", href = re.compile("^(/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages and link.attrs['href'] not in playerLinks:
                newPage = link.attrs['href']
                print(newPage)
                r"(\/spieler\/)[a-z+]*\-[a-z+]*\-[0-9]{6}"
                if re.match(r"(\/spieler\/)[a-z+\-]*[0-9]{5,6}", newPage) is not None:
                    print("Player found")
                    playerLinks.add(newPage)
                    pages.add(newPage)
                    playersFile.write(newPage+"\n")
                else:
                    pages.add(newPage)
                    getLinks(newPage)

# da recursion error erzeugt: maximum recursion depth exceeded in comparison
# stack verwenden oder collections push und pop!


def stackVersuch():
    print("Stack size:", stack.size())
    getLinksStack(stack.pop())

def handleLinks(newPage):
    global pages
    global playerLinks
    print(newPage)
    if re.match(r"(\/spieler\/)[a-z+\-]*[0-9]{5,6}", newPage) is not None:
        print("Player found")
        playerLinks.add(newPage)
        pages.add(newPage)
        playersFile.write(newPage + "\n")
    # da sonst falsche Links bestehen und das Programm in eine Dauerschleife läuft
    elif ("?" in newPage or "&" in newPage):
        print("False Link!")
        pages.add(newPage)
    else:
        pages.add(newPage)
        stack.push(newPage)

def getLinksStack(pageURL):
    # global variable use the global variable from the beginning
    global pages
    global playerLinks
    #req = session.get(url+"/club/jsg-union-dessau/calender/2030-03/club/sportunion-wacker-sued/calender/2018-10", headers=headers) #for testing
    req = session.get(url + pageURL, headers=headers)
    bsObj = BeautifulSoup(req.text, "html.parser")

    # re = regular expression
    # re.compile compile to a regular expression object
    for link in bsObj.find_all("a", href = re.compile("^(/)")):
        if 'href' in link.attrs:
            if (link.attrs['href'] not in pages and link.attrs['href'] not in playerLinks):
                if 'id' in link.attrs:
                    if re.match(r"(navi_link_)[0-9]{1,3}", link.attrs['id']) is not None:
                        handleLinks(link.attrs['href'])
                elif ((re.match(r"(.*/liga/).*", link.attrs['href'])or re.match(r"(.*/club/).*", link.attrs['href']) or re.match(r"(/spieler/)[a-z+\-]*[0-9]{5,6}", link.attrs['href']) is not None)
                    and (re.match(r"(.*/calender).*", link.attrs['href']) is None)):
                    #re.match(r"(.*\/calender).*", link.attrs['href']) or re.match(r"(.*\/spielberichte\/).*", link.attrs['href'])is None:
                    #re.match(r"/[a-z+][^/]", link.attrs['href'])
                    handleLinks(link.attrs['href'])
                else:
                    print("Wrong Like - Don't look at it")
            else:
                print("Link already exist!")




nodesAlreadyVisited = set()
playerNodes = set()


def getLinksNode(node):
    # req = session.get(url+"/club/jsg-union-dessau/calender/2030-03/club/sportunion-wacker-sued/calender/2018-10",
    # headers=headers)
    # for testing
    req = session.get(url + node, headers=headers)
    nodes = BeautifulSoup(req.text, "html.parser")

    return nodes


def searchBreadth(depth, nodes):
    noDepth = 0
    firstDepth = 1
    secondDepth = 2
    thirdDepth = 3
    nodeLink = ""

    print("Depth: ", depth)

    if nodes is None or len(nodes) == 0:
        print("keine Nodes mehr vorhanden!")
    else:
        for node in nodes.find_all("a", href = re.compile("^(/)")):
            if (node.attrs['href'] not in nodesAlreadyVisited and node.attrs['href'] not in playerNodes):
                nodeLink = node.attrs['href']
                if depth == noDepth:
                    if 'id' in node.attrs:
                        if re.match(r"(navi_link_)[0-9]{1,3}", node.attrs['id']) is not None:
                            print(nodeLink)
                            searchBreadth(depth+1, getLinksNode(nodeLink))
                elif depth == firstDepth:
                    if re.match(r"(.*/liga/).*", node.attrs['href']) is not None:
                        print(nodeLink)
                        searchBreadth(depth + 1, getLinksNode(nodeLink))
                elif depth == secondDepth:
                    if re.match(r"(.*/club/).*", node.attrs['href']) is not None:
                        print(nodeLink)
                        searchBreadth(depth + 1, getLinksNode(nodeLink))
                elif depth == thirdDepth:
                    if re.match(r"(/spieler/)[a-z+\-]*[0-9]{5,6}", node.attrs['href']) is not None:
                        print("Player found")
                        playerNodes.add(nodeLink)
                        nodesFile.write(nodeLink+"\n")
                else:
                    print("Depth zu Tief!! Depth: ", depth)

            nodesAlreadyVisited.add(node)


searchBreadth(0, getLinksNode(""))



# secondPage()
# versuch()
# getLinks("")
# print(playerLinks)


#getLinksStack("")

#while (!stack.isEmpty()):
#while stack.size()>0:
    #stackVersuch()
