import csv
from nltk import WhitespaceTokenizer
import re
from difflib import SequenceMatcher


class GatherInformation:

    def __init__(self):
        self.database_word_list_hobbies = []
        self.database_word_list_location = []
        self.database_word_list_occupation = []
        self.database_word_list_institutions = []
        self.location = []
        self.hobbies = []
        self.occupation = []
        self.institution = []
        self.whitespace_wt = WhitespaceTokenizer()
        self.emails = []

    # find locations in keywords
    def compare_keywords_with_locations(self, keywords):
        with open('location.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            for row in csv_reader:
                if len(row)<1:
                    continue
                else:
                    self.database_word_list_location.append(row[0].lower())
            for word in keywords:
                for element in self.database_word_list_location:
                    if element == word:
                        self.location.append(element)
        if self.location:
            print("Gefundene Orte: ", self.location)
            return self.location
        return -1


    # find hobbies in keywords
    def compare_keywords_with_hobbies(self, keywords):
        with open('hobbies.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            for row in csv_reader:
                self.database_word_list_hobbies.append(row[0].lower())
            for word in keywords:
                for element in self.database_word_list_hobbies:
                    if element == word:
                        self.hobbies.append(element)
        if self.hobbies:
            print("Gefundene Hobbies: ", self.hobbies)
            return self.hobbies
        return -1

    # find occupations in keywords
    def compare_keywords_with_occupations(self, keywords):
        with open('occupations.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            for row in csv_reader:
                if len(row)<1:
                    continue
                else:
                    self.database_word_list_occupation.append(row[0].lower())
            for word in keywords:
                for element in self.database_word_list_occupation:
                    if element == word:
                        self.occupation.append(element)
        #return most_often_occupation
        if self.occupation:
            print("Gefundene Tätigkeiten: ", self.occupation)
            return self.occupation
        else:
            return -1

    # find institutions in keywords
    def compare_keywords_with_institutions(self, html_string):
        text = str(html_string)
        with open('institutions.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile, delimiter=',', quotechar='"')
            for row in csv_reader:
                if len(row)<1:
                    continue
                else:
                    self.database_word_list_institutions.append(row[0])
            for element in self.database_word_list_institutions:
                if element in text:
                    self.institution.append(element)

        if self.institution:
            print("Gefundene Institutionen: ", self.institution)
            return self.institution
        else:
            return -1

    # check the found emails and choose the right one
    def compare_email_with_name(self, firstname, secondname, mail):
        formatted_name = firstname.lower()+secondname.lower()
        local_part_of_mailaddress = mail.split("@")[0].lower()
        percentage_limit = 0.5
        print("Score",SequenceMatcher(None, formatted_name, local_part_of_mailaddress).ratio())
        if SequenceMatcher(None, formatted_name, local_part_of_mailaddress).ratio()>= percentage_limit:
            formatted_mail = mail.replace("(at)","@")
            if formatted_mail not in self.emails:
                self.emails.append(formatted_mail)

    # search for emails in website text
    def get_email(self, html_string, firstname, secondname):
        email_words = self.whitespace_wt.tokenize(html_string.lower())
        for fragment in email_words:
            mail_regex = re.search('(.*((@)|(\(at\))).*\.(de|com|net)).*', fragment)
            if mail_regex:
                print("Nicht überprüfte Email gefunden: ", mail_regex.group(1))
                self.compare_email_with_name(firstname, secondname, mail_regex.group(1))
        if self.emails:
            print("Korrekte Emails gefunden: ", self.emails)
            return self.emails
        else:
            return -1

    # search for the year of birth
    def get_years(self, keywords):
        regex_string = "(geburtsdatum)|(alter)|(geboren)|(geburtsort)|(born)|(birth)"
        all_years_in_text = []
        year_length = 4
        for element in keywords:
            if re.match(r"[0-9]{4}", element) and len(element) == year_length:
                if 1900 <= int(element) <= 2019 and not element in all_years_in_text:
                    all_years_in_text.append(element)

        if all_years_in_text:
            print("Gefundene Jahreszahlen: ",all_years_in_text)
            for year in all_years_in_text:
                vistited_elements = 1
                max_number_of_visited_elements = 15
                #  to get all occurrences of this year
                occurrences = [i for i, x in enumerate(keywords) if x == year]
                for position_of_year in occurrences:
                    while (position_of_year+vistited_elements) < len(
                            keywords)-1 and vistited_elements <= max_number_of_visited_elements and position_of_year is not -1:
                        index_behind = position_of_year+ vistited_elements
                        index_front = position_of_year - vistited_elements
                        if re.match(r""+regex_string, keywords[index_front]):
                            print("Front: Geburtsjahr wurde gefunden", year)
                            return year
                        elif re.match(r""+regex_string, keywords[index_behind]):
                            print("Behind: Geburtsjahr wurde gefunden", year)
                            return year
                        vistited_elements += 1
        return -1
