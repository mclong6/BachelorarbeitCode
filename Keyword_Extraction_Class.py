from nltk import word_tokenize
from nltk import WhitespaceTokenizer
from collections import Counter
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from nltk import ngrams
import csv
from rake_nltk import Rake, Metric



german_stopwords = stopwords.words('german')
english_stopwords = stopwords.words("english")
r = Rake(language="german",stopwords=german_stopwords, ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO,max_length=4)

#https://www.pc-erfahrung.de/nebenrubriken/sonstiges/webdesignwebentwicklung/stoppwortliste.html

browser = webdriver.Chrome('/home/marco/Downloads/chromedriver')
browser.implicitly_wait(10)
stemmer = SnowballStemmer('german')
stemmed_words = []
all_bigrams = []
whitespace_wt = WhitespaceTokenizer()


def formate_input_text(html_string):
    formatted_string = html_string.replace("\\n", "")
    formatted_string = re.sub('[!"|?&#/$()\',\-}{;:*+_[\]=]', '', formatted_string)
    formatted_string = re.sub(r"(\w)([A-Z])", r"\1 \2", formatted_string)
    formatted_string = re.sub(r"(\w)([0-9])", r"\1 \2", formatted_string)
    formatted_string = re.sub(r' [0-9]{1,3} ', '', formatted_string)
    formatted_string = re.sub(r' [a-z]{1,2} ', '', formatted_string)

    print("FINAL",formatted_string)
    return formatted_string


def get_email(html_string):
    email_words = whitespace_wt.tokenize(html_string.lower())
    for element in email_words:
        #element = "lang@pw-metallbau.de"
        if re.match(r".*@.*\.(de|com|net)", element) is not None:
            print("Email found:"+ element)

browser.get("https://www.schwaebische.de/landkreis/bodenseekreis/tettnang_artikel,-junge-union-will-partty-bus-verwirklichen-_arid,10701303.html")
html_of_search = browser.page_source
html = BeautifulSoup(html_of_search, "html.parser")
html_string = str(html.body.text)
html_string = formate_input_text(html_string)

r.extract_keywords_from_text(html_string)

print(r.get_ranked_phrases())
print(r.get_ranked_phrases_with_scores())
print(r.get_word_degrees())
print(r.get_word_frequency_distribution())
