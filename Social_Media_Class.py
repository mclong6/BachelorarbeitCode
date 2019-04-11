from bs4 import BeautifulSoup
import re
import time
from selenium.webdriver.common.by import By
import Keyword_Extraction_Class
import Gather_Information_Class
import random
from selenium import webdriver
import Handle_Google_Results_Class
# Mechanize cannot execute javascript and send asynchronous requests, but Selenium can do it;If you want to scrap a
# static website, Mechanize is better(provides friendly apis and quickly);If you want to scrap any SPA(like AngularJS,
# ReactJS,VueJS) website, Selenium can help you;If you need to auto login, it depends the web page needs to execute JS
# or not.
class Person(object):
    def __init__(self):
        self.first_name = ""
        self.second_name = ""
        self.place_of_residence = ""
        self.year_of_birth = ""
        self.estimated_year_of_birth = ""
        self.institution = ""
        self.instagram_name = ""
        self.facebook_name = ""
        self.twitter_name = ""
        self.occupation = []
        self.hobbies = []
        self.universities = []
        self.email = []
        self.locations = []
        self.contacts_information = []
        self.institution_founded = []

class SocialMedia:
    def __init__(self):
        self.username = "bachelorarbeit2@gmx.de"
        self.password = "bachelorarbeit2"
        self.fb_username = "bachelorarbeitIT@gmx.de"
        self.fb_password = "bachelorarbeitFB"
        self.instagram_key = 1
        self.facebook_key = 2
        self.twitter_key = 3
        self.linkedin_key = 4
        self.xing_key = 5
        self.facebook_login_page = "https://www.facebook.com/login/"
        self.instagram_login_page = "https://www.instagram.com/accounts/login/?next=%2Fbachelor_arbeit2%2F&source=desktop_nav"
        self.xing_login_page = "https://login.xing.com/login"
        self.linkedin_login_page = "https://www.linkedin.com/uas/login"
        self.twitter_login_page = "https://twitter.com/login"
        self.browser = webdriver.Chrome('/home/marco/Downloads/chromedriver')
        self.browser.implicitly_wait(10)
        self.url = ""
        self.links_to_contacts = []
        self.instagram_login = False
        self.facebook_login = False
        self.twitter_login = False
        self.person_object = Person()

    def handle_social_media(self, person):
        print("handle_social_media()")
        self.transfer_information(person)
        if self.person_object.first_name and self.person_object.second_name and self.person_object.place_of_residence:
            self.search_linkedin()
            self.search_xing()
        if self.person_object.instagram_name:
            self.login_to_any_page(self.instagram_key)
            self.instagram_login = True
            if not self.check_person_information():
                self.handle_instagram(False)
            else:
                self.handle_instagram(True)
        if self.person_object.twitter_name:
            self.login_to_any_page(self.twitter_key)
            self.twitter_login = True
            if not self.check_person_information():
                self.handle_twitter(False)
            else:
                self.handle_twitter(True)
        #if self.person_object.facebook_name:
            #self.handle_facebook()
        return self.person_object

    def transfer_information(self, social_media_person):
        self.person_object.first_name = social_media_person.first_name
        self.person_object.second_name = social_media_person.second_name
        self.person_object.place_of_residence = social_media_person.place_of_residence
        self.person_object.institution = social_media_person.institution
        self.person_object.year_of_birth = social_media_person.year_of_birth
        self.person_object.estimated_year_of_birth = social_media_person.estimated_year_of_birth
        self.person_object.twitter_name=social_media_person.twitter_name
        self.person_object.facebook_name = social_media_person.facebook_name
        self.person_object.instagram_name = social_media_person.instagram_name
        self.person_object.institution_founded = social_media_person.institution_founded

    def search_linkedin(self):
        print("in search linkedin")
        links_to_person = []
        self.login_to_any_page(self.linkedin_key)
        search_link_list = self.create_search_links(self.linkedin_key)
        print(search_link_list[0])
        self.browser.get(search_link_list[0])
        html_of_search = self.browser.page_source
        html_soup = BeautifulSoup(html_of_search, "html.parser")
        #links = html_soup.find_all("a",{"id": re.compile("(ember)[0-9]*")})
        links = html_soup.find_all("a", {"href": re.compile("(/in/)[(w)]*")})
        for link in links:
            if link.attrs["href"] not in links_to_person:
                links_to_person.append(link.attrs["href"])
        print(links_to_person)
        #TODO Create Alogrithmus to know which person is the vitim
        if len(links_to_person) == 1:
            url = "https://www.linkedin.com"+links_to_person[0]
            self.handle_social_media_url(url)
        #TODO delet Ravensurg-Weingarten if it is wrong
            """if self.person_object.locations[1] == "weingarten" and self.person_object.locations[0] == "ravensburg":
                print("TRUEEEEEEEEEE")
            else:
                del self.person_object.locations[self.person_object.locations.index("weingarten")]
                del self.person_object.locations[self.person_object.locations.index("ravensburg")]"""

            print("Locations: ",self.person_object.locations)

    def search_xing(self):
        links_to_person = []
        self.login_to_any_page(self.xing_key)
        search_link_list = self.create_search_links(self.xing_key)
        print(search_link_list[0])
        time.sleep(2)
        self.browser.get(search_link_list[0])

        html_of_search = self.browser.page_source
        html_soup = BeautifulSoup(html_of_search, "html.parser")
        # links = html_soup.find_all("a",{"id": re.compile("(ember)[0-9]*")})
        links = html_soup.find_all("a", {"href": re.compile("(/profile/).*/.*")})
        for link in links:
            if link.attrs["href"] not in links_to_person:
                links_to_person.append(link.attrs["href"])
        print(links_to_person)
        # TODO Create Alogrithmus to know which person is the vitim
        if len(links_to_person) == 1:
            url = "https://www.xing.com" + links_to_person[0]
            self.handle_social_media_url(url)

    def login_to_any_page(self, key):
        if key == self.instagram_key or key == self.linkedin_key:
            if key == self.instagram_key:
                self.url = self.instagram_login_page
            elif key == self.linkedin_key:
                self.url = self.linkedin_login_page
            self.browser.maximize_window()
            self.browser.get(self.url)
            time.sleep(2)
            html_of_search = self.browser.page_source
            html = BeautifulSoup(html_of_search, "html.parser")
            input_username = html.find("input", {'type': re.compile("^(text)|(email)")})
            input_password = html.find("input", {"type": "password"})
            # time.sleep(1)
            self.browser.find_element_by_id(input_username.attrs["id"]).send_keys(self.username)
            self.browser.find_element_by_id(input_password.attrs["id"]).send_keys(self.password+"\n")
            time.sleep(2)

        elif key == self.twitter_key:
            self.url = self.twitter_login_page
            self.browser.maximize_window()
            self.browser.get(self.url)
            time.sleep(1)
            html_of_search = self.browser.page_source
            html = BeautifulSoup(html_of_search, "html.parser")
            input_username = html.find("input", {'class': "js-username-field email-input js-initial-focus"})
            input_password = html.find("input", {"class": "js-password-field"})
            username_class = input_username.attrs["class"][0]
            password_class = input_password.attrs["class"][0]
            time.sleep(1)
            self.browser.find_element_by_class_name(username_class).send_keys(self.username)
            self.browser.find_element_by_class_name(password_class).send_keys(self.password+"\n")
            time.sleep(2)

        elif key == self.xing_key:
            self.url = self.xing_login_page
            self.browser.maximize_window()
            self.browser.get(self.url)
            time.sleep(1)
            html_of_search = self.browser.page_source
            html = BeautifulSoup(html_of_search, "html.parser")
            input_username = html.find("input", {'type': re.compile("^(text)|(email)")})
            input_password = html.find("input", {"type": "password"})
            # time.sleep(1)
            self.browser.find_element_by_name(input_username.attrs["name"]).send_keys(self.username)
            self.browser.find_element_by_name(input_password.attrs["name"]).send_keys(self.password + "\n")

    def handle_instagram(self, is_name_known):
        print("handle_instagram()", is_name_known)
        search_url_list = self.create_search_links(self.instagram_key)
        url_to_profil = search_url_list[0]
        url_to_further_information = search_url_list[1]

        # handle profile site
        self.handle_social_media_url(url_to_profil)
        #is accunt private or not
        html_of_search = self.browser.page_source
        html_soup = BeautifulSoup(html_of_search, "html.parser")
        #To get personen first and second name, only username is given
        if not is_name_known:
            person_name = str(html_soup.find("h1", attrs={"class": "rhpdm"}).text).lower().split()
            if len(person_name)>1:
                self.person_object.first_name = person_name[0]
                self.person_object.second_name = person_name[1]
            else:
                self.person_object.first_name = person_name[0]
        print(self.person_object.first_name,self.person_object.second_name)

        #To find out if it is a private account or not
        if html_soup.find_all(text="Dieses Konto ist privat"):
            print("Dieses Konto ist privat!!!")
            # Just for testing
            self.get_contacts_private_account(self.instagram_key, )
        else:
            self.get_contacts_public_account()

        # handle_further_information
        self.browser.get(url_to_further_information)
        html_of_search = self.browser.page_source
        handle_google_results_class = Handle_Google_Results_Class.HandleGoogleResults()
        links_to_scrape = handle_google_results_class.handle_google_results(html_of_search)
        print(links_to_scrape)
        for link in links_to_scrape:
            self.handle_social_media_url(link)

    def handle_twitter(self, is_name_known):
        print("handle_twitter()")
        search_url_list = self.create_search_links(self.twitter_key)
        self.handle_social_media_url(search_url_list[0])
        html_of_search = self.browser.page_source
        html_soup = BeautifulSoup(html_of_search, "html.parser")
        #To get personen first and second name, only username is given
        if not is_name_known:
            person_name = str(html_soup.find("a", attrs={"class": "ProfileHeaderCard-nameLink u-textInheritColor js-nav"}).text).lower().split()
            if len(person_name) > 1:
                self.person_object.first_name = person_name[0]
                self.person_object.second_name = person_name[1]
            else:
                self.person_object.first_name = person_name[0]
        print("HandleTWITTER:",self.person_object.first_name, self.person_object.second_name)

    def handle_facebook(self):
        print("handle_facebook()")
        search_link_list = self.create_search_links(self.facebook_key)
        for url in search_link_list:
            self.handle_social_media_url(url)

    def handle_social_media_url(self, url):
        url = url.split("%",1)[0]
        print(url)
        self.browser.get(url)
        time.sleep(2)
        html_of_search = self.browser.page_source
        html_soup = BeautifulSoup(html_of_search, "html.parser")
        self.gather_information(html_soup.text)

    def gather_information(self, text):
        keyword_extraction_class = Keyword_Extraction_Class.KeywordExtraction()
        formatted_text = keyword_extraction_class.formate_input_text(text)
        keywords = keyword_extraction_class.create_keywords(formatted_text)
        gather_information_class = Gather_Information_Class.GatherInformation()
        self.person_object.hobbies.append(gather_information_class.compare_keywords_with_hobbies(keywords))
        self.person_object.locations.append(gather_information_class.compare_keywords_with_locations(keywords))
        self.person_object.institution_founded.append(gather_information_class.compare_keywords_with_institutions(keywords))
        self.person_object.occupation.append(gather_information_class.compare_keywords_with_occupations(keywords))

    def check_person_information(self):
        is_name = False
        if self.person_object.first_name and self.person_object.second_name:
            is_name = True
        return is_name

    def get_contacts_public_account(self):
        print("get_contacts_public_account()")
        #self.person_object.hobbies.append("fußball")
        html_of_search = self.browser.page_source
        html_soup = BeautifulSoup(html_of_search, "html.parser")
        username = html_soup.find("h1")
        follower_atag = html_soup.find("a", attrs={"href": re.compile("/.*(/followers/)")})
        information_tags = self.browser.find_elements_by_class_name(follower_atag.attrs["class"][0])
        information_tags[2].click()
        time.sleep(2)
        html_of_search = self.browser.page_source
        html_soup = BeautifulSoup(html_of_search, "html.parser")
        print(html_soup.prettify())
        #for link in html_soup.find_all("a",attrs={"class": re.compile("(FPmhX notranslate _0imsa)|(_2dbep qNELH kIKUG)")}):
        for link in html_soup.find_all("a", attrs={"class": re.compile("(FPmhX notranslate _0imsa)")}):
            print(link.attrs["href"])
        # Find the pop-up window
        pop_up = self.browser.find_element_by_xpath('/html/body/div[2]/div/div[2]')        # find number of followers
        all_following = int(self.browser.find_element_by_xpath("//li[2]/a/span").text)
        # scroll down the page
        print("FOLLOWER",all_following)
        print("RANGE:",int(all_following / 6))
        for i in range(int(all_following / 6)):
            if i == 0:
                self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/5", pop_up)
                time.sleep(2)
            else:
                self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pop_up)
            time.sleep(random.randint(500, 1000) / 1000)
            #print("Extract friends %", round((i / (all_following / 2) * 100), 2), "from", "%100")
        html_of_search= self.browser.page_source
        html_soup = BeautifulSoup(html_of_search, "html.parser")
        for link in html_soup.find_all("a", attrs={"class": re.compile("(FPmhX notranslate _0imsa)")}):
            print(link.attrs["href"])
            self.links_to_contacts.append(link.attrs["href"])
        self.get_contacts_information()

    def get_contacts_private_account(self, key):
        if key == self.instagram_key:
            try:
                while 1:
                    html_of_search = self.browser.page_source
                    html_soup = BeautifulSoup(html_of_search, "html.parser")
                    for div in html_soup.find_all("div", attrs={"class":"_41KYi LQtnO"}):
                            for a_tag in div.find_all("a", attrs={'href': re.compile("/[a-z0-9.\-_]/*")}):
                                #print(a_tag.attrs["href"])
                                if a_tag.attrs["href"] not in self.links_to_contacts:
                                    self.links_to_contacts.append(a_tag.attrs["href"])
                                    print(self.links_to_contacts)
                    self.browser.find_element_by_xpath("//*[@class='Szr5J  _6CZji']").click()
            except Exception as e:
                print("no more links")
                print(e)

    def get_contacts_information(self):
        for contact_link in self.links_to_contacts:
            print(contact_link)
            url = "https://www.instagram.com" + contact_link
            self.browser.get(url)
            html_of_search = self.browser.page_source
            html_soup = BeautifulSoup(html_of_search, "html.parser")
            #Section or whole HTML???
            sections = html_soup.find_all("section")
            print(sections[1].text)

            keyword_extraction_class = Keyword_Extraction_Class.KeywordExtraction()
            formatted_text = keyword_extraction_class.formate_input_text(sections[1].text)
            keywords = keyword_extraction_class.create_keywords(formatted_text)
            gather_information_class = Gather_Information_Class.GatherInformation()
            hobbies_of_contact = gather_information_class.compare_keywords_with_hobbies(keywords)
            locations_of_contact = gather_information_class.compare_keywords_with_locations(keywords)
            universities_of_contact = gather_information_class.compare_keywords_with_institutions(keywords)
            occupations_of_contact = gather_information_class.compare_keywords_with_occupations(keywords)

            if self.compare_contact_information(html_soup,hobbies_of_contact,locations_of_contact,universities_of_contact,occupations_of_contact):
                break
        print(self.person_object.contacts_information)

    def compare_contact_information(self,html_soup, hobbies_of_contact,locations_of_contact,universities_of_contact,
                                    occupations_of_contact):
        if self.person_object.place_of_residence in locations_of_contact:
            print("Same Location: ", self.person_object.place_of_residence)
            contact_name = html_soup.find("h1", attrs={"class": "rhpdm"}).text
            self.person_object.contacts_information.append(contact_name)
            self.person_object.contacts_information.append(self.person_object.place_of_residence)
            return True
        for hobbie in self.person_object.hobbies:
            if hobbie in hobbies_of_contact:
                print("Same Hobbie")
                contact_name = html_soup.find("h1", attrs={"class": "rhpdm"}).text
                self.person_object.contacts_information.append(contact_name)
                self.person_object.contacts_information.append(hobbie)
                return True
        for university in self.person_object.universities:
            if university in universities_of_contact:
                print("Same University")
                contact_name = html_soup.find("h1", attrs={"class": "rhpdm"}).text
                self.person_object.contacts_information.append(contact_name)
                self.person_object.contacts_information.append(university)
                return True
        for occupation in self.person_object.occupation:
            if occupation in occupations_of_contact:
                print("Same University")
                contact_name = html_soup.find("h1", attrs={"class": "rhpdm"}).text
                self.person_object.contacts_information.append(contact_name)
                self.person_object.contacts_information.append(occupation)
                return True
        return False


    def create_search_links(self, key):
        search_url_list = []
        if key == self.instagram_key:
            search_url_list.append("https://www.instagram.com/" + self.person_object.instagram_name + "/")
            search_url_list.append("https://www.google.com/search?q=site%3Ainstagram.com+%22"+
                                   self.person_object.instagram_name + "%22+-site%3Ainstagram.com%2F" +
                                   self.person_object.instagram_name + "&oq=site%3Ainstagram.com+%22" +
                                   self.person_object.instagram_name + "%22+-site%3Ainstagram.com%2F" +
                                   self.person_object.instagram_name)

        elif key == self.twitter_key:
            search_url_list.append("https://twitter.com/"+ self.person_object.twitter_name)

        elif key == self.linkedin_key:
            search_url_list.append("https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22de%3A0%22%5" +
                                   "D&keywords="+self.person_object.first_name+"%20" +
                                   self.person_object.second_name+"%20"+self.person_object.place_of_residence +
                                   "&origin=FACETED_SEARCH")
        elif key == self.xing_key:
            search_url_list.append("https://www.xing.com/search/old/members?hdr=1&keywords="
                                   +self.person_object.first_name+"+"+self.person_object.second_name+
                                   "+"+self.person_object.place_of_residence)

        elif key == self.facebook_key:
            search_url_list.append("https://www.facebook.com/search/str/"+self.person_object.facebook_name+"/users-named")
            #TODO have look in OSINT BOOK to find further links with location
        return search_url_list

"""
test = SocialMedia()
#test.handle_instagram()
test.handle_social_media("test")

"""
