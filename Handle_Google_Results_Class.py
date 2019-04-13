from bs4 import BeautifulSoup
import re


class HandleGoogleResults:

    def handle_google_results(self, response):
        links_to_scrape = []

        if isinstance(response, str):
            obj = BeautifulSoup(response, "html.parser")
        else:
            obj = BeautifulSoup(response.text, "html.parser")
        result_div_list = obj.find_all("div", attrs={"class": "g"})

        for result_div in result_div_list:
            a_tag = result_div.find("a", attrs={'href': re.compile("(/url).*|(http).*")})
            if a_tag:
                # to remove /urlßq= from link, otherwise scrapy can't handle it
                formatted_url = str(a_tag.attrs['href']).replace("/url?q=", "").split("&",1)[0]
                if not formatted_url in links_to_scrape:
                    links_to_scrape.append(formatted_url)
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
