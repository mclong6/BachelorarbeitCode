from rake_nltk import Rake, Metric
from nltk import WhitespaceTokenizer
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from selenium import webdriver
from bs4 import BeautifulSoup

german_stopwords = stopwords.words('german')


r = Rake(language="german",stopwords=german_stopwords, ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO,max_length=4)
r_degree = Rake(language="german", stopwords=german_stopwords,ranking_metric=Metric.WORD_DEGREE,max_length=4)
r_frequency = Rake(language="german", stopwords=german_stopwords,ranking_metric=Metric.WORD_FREQUENCY,max_length=4)

browser = webdriver.Chrome('/home/marco/Downloads/chromedriver')
browser.implicitly_wait(10)
browser.get("https://businesspf.hs-pforzheim.de/studium/studierende/bachelor/bw_einkauf_logistik/studierende/studentisches_leben/")
html_of_search = browser.page_source
html = BeautifulSoup(html_of_search, "html.parser")
html_string = str(html.body.text)

text = "Auch wenn Sie sich nicht aktiv engagieren wollen, können Sie an den regelmäßigen Exkursionen der Studentengruppe" \
       " teilnehmen und Unternehmen kennen lernen, die gerne Praktikanten und Absolventen aus Pforzheim als Kollegen begrüßen. " \
       "Über anstehende Exkursionen informieren wir Sie auf unserer News-Seite. Und wenn Sie einfach nur mal einen geselligen Abend" \
       " mit vielen Gleichgesinnten verbringen wollen? Prima! Dann kommen Sie zum Logistiker-Stammtisch, der einmal im Semester stattfindet." \
       " Infos auf unserer News-Seite. Seit dem 28.03.2018 gibt es eine neue Hochschulgruppe im Studiengang Einkauf und Logistik. " \
       "Die Idee zu Logistik Live, kurz LogLive, entstand Mitte 2017, nachdem seit 2015 aufgrund fehlender finanzieller " \
       "Mittel keine Exkursionen mehr stattfinden konnten. Hier möchten wir etwas ändern. Jedes Semester sollen künftig bis" \
       " zu zwei Exkursionen zu Firmen in der näheren Umgebung organisiert werden, also im Großraum Karlsruhe, Pforzheim " \
       "und Stuttgart. Das Angebot richtet sich vor allem an Studentinnen und Studenten des 3. bis 5. Semesters, generell" \
       " ist aber jeder willkommen. Bei Fragen oder Anregungen oder Interesse an der Mitarbeit könnt Ihr gerne die beiden " \
       "BEL-Studenten und Initiatoren Nicole Schneider und Michael Fürer ansprechen. Wir freuen uns auf spannende Exkursionen " \
       "mit Euch. "

r.extract_keywords_from_text(html_string)
r_degree.extract_keywords_from_text(html_string)
r_frequency.extract_keywords_from_text(html_string)


print(r.get_ranked_phrases())
print(r_degree.get_ranked_phrases())
print(r_frequency.get_ranked_phrases())