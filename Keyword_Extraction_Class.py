from nltk import word_tokenize
from nltk.corpus import stopwords
import re
from nltk import ngrams
import html2text


# In this class the keywords are generated from the webpage text
class KeywordExtraction:

    def __init__(self):
        self.german_stopwords = stopwords.words('german')
        self.english_stopwords = stopwords.words("english")
        self.keywords = []

    def formate_input_text(self, input_string):
        h = html2text.HTML2Text()
        formatted_string = h.handle(input_string)
        formatted_string = formatted_string.replace("\n", " ")
        formatted_string = formatted_string.replace("ß","ss")

        formatted_string = re.sub(r'[><!"|?&#/$()\'\-,.}{;:*+_[\]=]', ' ', formatted_string)
        formatted_string = re.sub(r"([A-Z])*([A-Z])", r"\1 \2", formatted_string)
        # formatted_string = re.sub(r"(\w)([A-Z])", r"\1 \2", formatted_string)
        # formatted_string = re.sub(r"(\w)([0-9])", r"\1 \2", formatted_string)
        # formatted_string = re.sub(r' [0-9]{1,3} ', ' ', formatted_string)
        formatted_string = re.sub(r' [a-z]{1,2} ', ' ', formatted_string)
        return formatted_string

    def create_keywords(self, input_string):
        splitted_words = word_tokenize(input_string.lower())

        for word in splitted_words:
            if word not in (self.german_stopwords or self.english_stopwords):
                self.keywords.append(word)

        # With ngrams it is possible to find elements with more words
        # only bigramms are created and added to the keywords
        bigramms = list(ngrams(self.keywords, 2))
        formatted_bigramms = [" ".join(ngram) for ngram in bigramms]
        self.keywords = self.keywords + formatted_bigramms

        print("Schlüsselwörter: ",self.keywords)
        return self.keywords
