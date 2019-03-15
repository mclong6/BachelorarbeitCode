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


german_stopwords = stopwords.words('german')
english_stopwords = stopwords.words("english")
#https://www.pc-erfahrung.de/nebenrubriken/sonstiges/webdesignwebentwicklung/stoppwortliste.html

browser = webdriver.Chrome('/home/marco/Downloads/chromedriver')
browser.implicitly_wait(10)
stemmer = SnowballStemmer('german')
stemmed_words = []
all_bigrams = []
whitespace_wt = WhitespaceTokenizer()


def compare_text_with_keywords(html_string):
    all_formatted_words = []
    all_stemmed_words = []

    # to split a string at uppercase, MarcoLang  will be Marco Lang
    splitted_string_by_uppercase = re.findall('[A-Z][^A-Z]*', html_string)
    string = str(splitted_string_by_uppercase)
    # formatted_string = string.replace(","," ").replace("'","").replace("[","").replace("]","").replace("\\n","")
    formatted_string = string.replace("\\n", "")  # to delete all line breaks
    splitted_words = word_tokenize(formatted_string.lower())
    for word in splitted_words:
        formatted_word = ''.join(e for e in word if (e.isalnum()))
        if formatted_word is not '':
            all_formatted_words.append(formatted_word)
    #print(all_formatted_words)
    # Viele Fehler, dadurch entstehen wörter die es nicht gibt.
    """for word in all_formatted_words:
        stemmed_words = stemmer.stem(word)
        all_stemmed_words.append(stemmed_words)
    """
    # With ngrams it is possible to count the occurence of more words
    bigrams = list(ngrams(splitted_words, 2))
    frequencies = Counter(all_formatted_words)
    all_counted_words = []
    for frequencies_word, count in frequencies.most_common():
        if frequencies_word in (german_stopwords or english_stopwords) or len(frequencies_word) < 2:
            continue
        # print(frequencies_word, count)
        all_counted_words.append(frequencies_word)
    # read csv file
    keyword_list = []
    #case for place of residence
    with open('tätigkeiten.csv', 'r') as csvFile:
    # with open('hobbies.csv', 'r') as csvFile:
        csv_reader = csv.reader(csvFile)
        for row in csv_reader:
            keyword_list.append(row[0].lower())
        for word in all_counted_words:
            for element in keyword_list:
                if element in  word:
                    print("Textwort: "+word+"\nWort aus Liste: "+element)


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

compare_text_with_keywords(html_string)
get_email(html_string)

