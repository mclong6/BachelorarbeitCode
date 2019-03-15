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
import html2text

class KeywordExtraction():

    def __init__(self):
        self.german_stopwords = stopwords.words('german')
        self.english_stopwords = stopwords.words("english")
        #https://www.pc-erfahrung.de/nebenrubriken/sonstiges/webdesignwebentwicklung/stoppwortliste.html

        #browser = webdriver.Chrome('/home/marco/Downloads/chromedriver')
        #browser.implicitly_wait(10)
        self.stemmer = SnowballStemmer('german')
        self.stemmed_words = []
        self.all_bigrams = []
        self.whitespace_wt = WhitespaceTokenizer()


    def formate_input_text(self, input_string):
        print("FORMATE_INPUT_TEXT")
        h = html2text.HTML2Text()
        #is it possible to ignore <script>??
        formatted_string = h.handle(input_string)
        formatted_string = formatted_string.replace("\n", " ")

        formatted_string = re.sub(r'[><!"|?&#/$()\'\-,.}{;:*+_[\]=]', ' ', formatted_string)
        formatted_string = re.sub(r"(\w)([A-Z])", r"\1 \2", formatted_string)
        # formatted_string = re.sub(r"(\w)([0-9])", r"\1 \2", formatted_string)
        # formatted_string = re.sub(r' [0-9]{1,3} ', ' ', formatted_string)
        formatted_string = re.sub(r' [a-z]{1,2} ', ' ', formatted_string)
        return formatted_string


    def get_email(self, html_string):
        email_words  = self.whitespace_wt.tokenize(html_string.lower())
        for element in email_words:
            #element = "lang@pw-metallbau.de"
            if re.match(r".*@.*\.(de|com|net)", element) is not None:
                print("Email found:"+ element)


    def create_keywords(self, input_string):
        print("CREATE_KEYWORDS")
        splitted_words = word_tokenize(input_string.lower())

        # Viele Fehler, dadurch entstehen wörter die es nicht gibt.
        """
        for word in splitted_words:
                stemmed_words = stemmer.stem(word)
                all_stemmed_words.append(stemmed_words)
        """
        # With ngrams it is possible to count the occurrence of more words, this could be helpful for handling company names
        """
        bigrams = list(ngrams(splitted_words, 2))
        """
        bigrams = list(ngrams(splitted_words, 2))
        formatted_bigrams = [" ".join(ngram) for ngram in bigrams]
        splitted_words = splitted_words + formatted_bigrams

        # Counting words is not necessary, there is no advantage
        """counted_words = []
        frequencies = Counter(splitted_words)
        for frequencies_word, count in frequencies.most_common():
            if frequencies_word in (german_stopwords or english_stopwords) or len(frequencies_word) <= 2:
                continue
            # print(frequencies_word, count)
            counted_words.append(frequencies_word)
        print(counted_words)
        """
        print(splitted_words)
        return splitted_words

    def create_ngrams(self, input_string):
        bigrams_list = []
        # With ngrams it is possible to count the occurrence of more words, this could be helpful for handling company names
        bigrams = list(ngrams(input_string, 2))
        string = [" ".join(ngram) for ngram in bigrams]
        print(string)
        #for grams in bigrams:
            #print(grams)
            #string = string.join(grams)

        """string = ""
            for gram in grams:
                string = string.join(gram)
            bigrams.append(string)
            """

        #print(bigrams)



"""
browser.get("https://www.schwaebische.de/landkreis/bodenseekreis/tettnang_artikel,-junge-union-will-partty-"
            "bus-verwirklichen-_arid,10701303.html")
html_of_search = browser.page_source
html = BeautifulSoup(html_of_search, "html.parser")
html_string = str(html.body.text)
create_keywords(formate_input_text(html_string))
"""

#html_string = test(html_string)

