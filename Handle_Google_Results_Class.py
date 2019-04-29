from bs4 import BeautifulSoup
import re


# In this class the Google search results are analyzed and the URLs to the found pages are extracted.
class HandleGoogleResults:

    def handle_google_results(self, response):
        links_to_scrape = []
        # check if response is string or not
        if isinstance(response, str):
            obj = BeautifulSoup(response, "html.parser")
        else:
            obj = BeautifulSoup(response.text, "html.parser")
        result_div_list = obj.find_all("div", attrs={"class": "g"})

        for result_div in result_div_list:
            a_tag = result_div.find("a", attrs={'href': re.compile("(/url).*|(http).*")})
            if a_tag:
                # to remove /url?q= from link, otherwise scrapy can't handle it
                formatted_url = str(a_tag.attrs['href']).replace("/url?q=", "").split("&",1)[0]
                if formatted_url not in links_to_scrape:
                    links_to_scrape.append(formatted_url)
        print("Links to scrape:", links_to_scrape)

        next_page_tags = obj.find_all("a", attrs={'class': "fl"})
        next_page_links = []
        if next_page_tags:  # check if list is not empty
            for links in next_page_tags:
                next_page_link = links.attrs['href']
                next_page_links.append(next_page_link)
            # Further pages could be crawled
            print("Further pages: ", next_page_links)
        else:
            print("No more pages to scrape!")
        return links_to_scrape