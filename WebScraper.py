from bs4 import BeautifulSoup
from urllib.error import HTTPError
import requests
import re
import csv

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
                    if re.match(r"(https://www.fupa.net/spieler/)[a-z+\-]*[0-9]{5,7}.*", formatted_link) is not None:
                        linksToPlayerCollection.add(formatted_link)
                        linkAlreadyVisitedCollection.add(formatted_link)
                        csv_data = [formatted_link]
                        with open('linksToPlayerFile.csv', 'a') as csvFile:
                            writer = csv.writer(csvFile)
                            #writer.writerow(csv_data)
                            writer.writerow(get_player_information(formatted_link))
                        csvFile.close()
                        # print("Player found and added to the list")
                else:
                    print("!!   Depth is to big  !! Depth: ", depth)


def get_playerlink_from_csvfile():
    with open('linksToPlayerFile.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            print(row)

    csvFile.close()


def get_player_information(url):
    html = get_new_html(url)
    records = []
    data_of_player_list =[]
    formatted_data_of_player_list = []

    td_tag = html.find("td", {'class': re.compile("^(stammdaten)")})
    name_array = td_tag.h1.text.split()  # to split the name in first and second name
    for name in name_array:
        data_of_player_list.append(name)
    if len(name_array) == 1:
        data_of_player_list.append('-')
        data_of_player_list.append('-')
    elif len(name_array) == 2:
        data_of_player_list.insert(1, '-')
    player_data_information =['Vorname:','Zweitname:','Nachname:']
    for row in td_tag.findAll("tr"):
        col = row.findAll("td")
        if col[0].text == '\n\n\n\n\n\n\n\n\n':
            club_array = col[1].text.split("\n")
            data_of_player_list.append(club_array[1])
            print('!!!!',club_array)
        else:
            data_of_player_list.append(col[1].text)
        player_data_information.append(col[0].text)

    example_list = ['Vorname:','Zweitname:','Nachname:','Spitzname:', 'Position:', 'Geburtsdatum:', 'Nationalität:', 'starker Fuß:', 'Größe:', 'Gewicht:', 'Profilaufrufe:', '\n\n\n\n\n\n\n\n\n']
    counter = 0

    for element1 in example_list:
        test_bool = False
        counter2 = 0
        for element2 in player_data_information:
            if element2 == element1:
                formatted_data_of_player_list.append(data_of_player_list[counter2])
                test_bool= True
                break
            counter2 = counter2 +1
        if not test_bool:
            formatted_data_of_player_list.insert(counter,"unbekannt")
        counter = counter + 1



    #print(player_data_information)
    print(formatted_data_of_player_list)
    return formatted_data_of_player_list

    # teststring = table_tag.h1.text
    # print(teststring)
    # print(table_tag.table.tr)


# search_breadth(noDepth, get_new_html(""))
search_breadth(fourthDepth, get_new_html("https://www.fupa.net/club/tsv-tettnang/team/m1"))
# get_playerlink_from_csvfile()
#get_player_information("https://www.fupa.net/spieler/nils-maurer-869238.html")


