from nltk import word_tokenize
from nltk import WhitespaceTokenizer
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import re
from nltk import ngrams
import html2text
import csv
from difflib import SequenceMatcher


class KeywordExtraction:

    def __init__(self):
        self.german_stopwords = stopwords.words('german')
        self.english_stopwords = stopwords.words("english")
        # further stoplists
        # https://www.pc-erfahrung.de/nebenrubriken/sonstiges/webdesignwebentwicklung/stoppwortliste.html

        self.stemmer = SnowballStemmer('german')
        self.stemmed_words = []
        self.all_bigrams = []
        self.whitespace_wt = WhitespaceTokenizer()
        self.keywords = []

    def formate_input_text(self, input_string):
        h = html2text.HTML2Text()
        # is it possible to ignore <script>??
        formatted_string = h.handle(input_string)
        formatted_string = formatted_string.replace("\n", " ")
        formatted_string = formatted_string.replace("ß","ss")

        formatted_string = re.sub(r'[><!"|?&#/$()\'\-,.}{;:*+_[\]=]', ' ', formatted_string)
        formatted_string = re.sub(r"([A-Z])*([A-Z])", r"\1 \2", formatted_string)
        # formatted_string = re.sub(r"(\w)([A-Z])", r"\1 \2", formatted_string)
        # formatted_string = re.sub(r"(\w)([0-9])", r"\1 \2", formatted_string)
        # formatted_string = re.sub(r' [0-9]{1,3} ', ' ', formatted_string)
        formatted_string = re.sub(r' [a-z]{1,2} ', ' ', formatted_string) #TODO weniger als zwei Zeichen versuchen z.B FH
        return formatted_string

    def create_keywords(self, input_string):
        splitted_words = word_tokenize(input_string.lower())

        for word in splitted_words:
            if word not in (self.german_stopwords or self.english_stopwords):
                self.keywords.append(word)

        # Viele Fehler, dadurch entstehen wörter die es nicht gibt.
        """
        for word in splitted_words:
                stemmed_words = stemmer.stem(word)
                all_stemmed_words.append(stemmed_words)
        """

        # With ngrams it is possible to count the occurrence of more words, this could be helpful for
        # handling company names
        # TODO create trigramms and Tetragrams, maybe Pentagramms
        # Maybe only bigramms, seperated query
        """bigramms = list(ngrams(self.keywords, 2))
        formatted_bigramms = [" ".join(ngram) for ngram in bigramms]
        self.keywords = self.keywords + formatted_bigramms"""



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
        print("KEYWORDS: ",self.keywords)
        return self.keywords


"""
browser.get("https://www.schwaebische.de/landkreis/bodenseekreis/tettnang_artikel,-junge-union-will-partty-"
            "bus-verwirklichen-_arid,10701303.html")
html_of_search = browser.page_source
html = BeautifulSoup(html_of_search, "html.parser")
html_string = str(html.body.text)
create_keywords(formate_input_text(html_string))
"""


