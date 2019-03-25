from bs4 import BeautifulSoup
import re


class HandleGoogleResults:

    def handle_google_results(self, response):
        links_to_scrape = []

        if isinstance(response, str):
            obj = BeautifulSoup(response, "html.parser")
        else:
            obj = BeautifulSoup(response.text, "html.parser")
        # TODO why is class name not r???
        result_div_list = obj.find_all("div", attrs={"class": "g"})
        # result_div_list = obj.find_all("div",class_:"r")

        # How do image results be handled?
        for result_div in result_div_list:
            a_tag = result_div.find("a", attrs={'href': re.compile("^.*")})
            links_to_scrape.append(a_tag.attrs['href'])
            print(a_tag.attrs['href'])
        print("Links to scrape:", links_to_scrape)

        next_page_tags = obj.find_all("a", attrs={'class': "fl"})
        # next_page_tags = obj.find_all("a", attrs={'aria-label': re.compile("^(Page )[0-9]{1,3}")})
        next_page_links = []
        if next_page_tags:  # check if list is not empty
            for links in next_page_tags:
                next_page_link = links.attrs['href']
                next_page_links.append(next_page_link)
            print("Further Pages: ", next_page_links)
            # TODO pages could be crawled
        else:
            print("No more pages to scrape!")
        # finally extend next_page_links to links_to_scrape
        return links_to_scrape
