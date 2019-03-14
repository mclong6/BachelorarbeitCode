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

text = "In einer jungen Wissenschaft wie der Informatik mit ihrer Vielschichtigkeit und ihrer unüberschaubaren " \
       "Anwendungsvielfalt ist man oftmals noch bestrebt, eine Charakterisierung des Wesens dieser Wissenschaft" \
       " und Gemeinsamkeiten und Abgrenzungen zu anderen Wissenschaften zu finden. Etablierte Wissenschaften haben" \
       " es da leichter, sei es, dass sie es aufgegeben haben, sich zu definieren, oder sei es, dass ihre Struktur " \
       "und ihre Inhalte allgemein bekannt sind."

def compare_text_with_keywords(text):
    all_formatted_words = []
    all_stemmed_words = []

    # to split a string at uppercase, MarcoLang  will be Marco Lang
    splitted_string_by_uppercase = re.findall('[A-Z][^A-Z]*', text)
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
    print(frequencies)
    print(frequencies.most_common())
    print(german_stopwords)
    words_without_stopwords = []
    for frequencies_word, count in frequencies.most_common():
        print(frequencies_word)
        if frequencies_word == "und":
            print("GLEICH")
        if frequencies_word not in german_stopwords:
            print("TEST")
            words_without_stopwords.append(frequencies_word)
    print("Keywords: ", words_without_stopwords)
    #for frequencies_word, count in frequencies.most_common():
        #if frequencies_word not in (german_stopwords or english_stopwords) or not len(frequencies_word) < 2:

        # print(frequencies_word, count)
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


compare_text_with_keywords(text)
