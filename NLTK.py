from nltk import word_tokenize
from collections import Counter
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from nltk import ngrams
german_stopwords = stopwords.words('german')
english_stopwords = stopwords.words("english")

browser = webdriver.Chrome('/home/marco/Downloads/chromedriver')
browser.implicitly_wait(10)
stemmer = SnowballStemmer('german')
stemmed_words=[]
all_bigrams = []

browser.get("https://www.xing.com/profile/Frederik_Nussbaumer/cv")
html_of_search = browser.page_source
html = BeautifulSoup(html_of_search, "html.parser")

html_string = str(html.body.text)
# to split a string at uppercase, MarcoLang  will be Marco Lang
splitted_string_by_uppercase = re.findall('[A-Z][^A-Z]*', html_string)
string = str(splitted_string_by_uppercase)
#formatted_string = string.replace(","," ").replace("'","").replace("[","").replace("]","").replace("\\n","")
formatted_string = string.replace("\\n","") #to delete all line breaks
splitted_words = word_tokenize(formatted_string.lower())

all_formatted_words = []
all_stemmed_words = []
for word in splitted_words:
    formatted_word = ''.join(e for e in word if e.isalnum())
    if formatted_word is not '':
        all_formatted_words.append(formatted_word)
print(all_formatted_words)
#Viele Fehler, dadurch entstehen wörter die es nicht gibt.
"""for word in all_formatted_words:
    stemmed_words = stemmer.stem(word)
    all_stemmed_words.append(stemmed_words)
"""
#With ngrams it is possible to count the occurence of more words
bigrams = list(ngrams(splitted_words, 2))

frequencies = Counter(all_formatted_words)
all_counted_words =[]
for frequencies_word, count in frequencies.most_common():
    if frequencies_word in (german_stopwords or english_stopwords) or len(frequencies_word) < 2:
        continue
    print(frequencies_word, count)
    all_counted_words.append(frequencies_word)

