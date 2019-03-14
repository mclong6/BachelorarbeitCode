from rake_nltk import Rake, Metric
from nltk import WhitespaceTokenizer
from nltk.stem import SnowballStemmer
import nltk
from nltk.corpus import stopwords
from selenium import webdriver
from bs4 import BeautifulSoup
nltk.download()
german_stopwords = stopwords.words('german')
english_stopwords = stopwords.words('english')
print(german_stopwords)
print(english_stopwords)

r = Rake(language="german",stopwords=german_stopwords, ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO,max_length=4)
#r_degree = Rake(language="german", stopwords=german_stopwords,ranking_metric=Metric.WORD_DEGREE,max_length=4)
#r_frequency = Rake(language="german", stopwords=german_stopwords,ranking_metric=Metric.WORD_FREQUENCY,max_length=4)
"""
browser = webdriver.Chrome('/home/marco/Downloads/chromedriver')
browser.implicitly_wait(10)
browser.get("https://businesspf.hs-pforzheim.de/studium/studierende/bachelor/bw_einkauf_logistik/studierende/studentisches_leben/")
html_of_search = browser.page_source
html = BeautifulSoup(html_of_search, "html.parser")
html_string = str(html.body.text)
"""
text = "In einer jungen Wissenschaft wie der Informatik mit ihrer Vielschichtigkeit und ihrer unüberschaubaren " \
       "Anwendungsvielfalt ist man oftmals noch bestrebt, eine Charakterisierung des Wesens dieser Wissenschaft" \
       " und Gemeinsamkeiten und Abgrenzungen zu anderen Wissenschaften zu finden. Etablierte Wissenschaften haben" \
       " es da leichter, sei es, dass sie es aufgegeben haben, sich zu definieren, oder sei es, dass ihre Struktur " \
       "und ihre Inhalte allgemein bekannt sind."

r.extract_keywords_from_text(text)

print(r.get_ranked_phrases())
print(r.get_ranked_phrases_with_scores())
print(r.get_word_degrees())
print(r.get_word_frequency_distribution())


#print(r_degree.get_ranked_phrases())
#print(r_frequency.get_ranked_phrases())