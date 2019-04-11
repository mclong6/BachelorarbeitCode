import csv
from nltk import WhitespaceTokenizer
import re
from difflib import SequenceMatcher
import datetime
import pattern3
import numpy


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
    # TODO ADD something like Jodel,Whatsapp,Snapchat ....

    def compare_keywords_with_locations(self, keywords):
        print(keywords)
        with open('location.csv', 'r') as csvFile:
            # with open('hobbies.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            for row in csv_reader:
                self.database_word_list_location.append(row[0].lower())
            for word in keywords:
                for element in self.database_word_list_location:
                    #if element in word:
                    if element == word:
                        #if word not in self.location:
                        self.location.append(element)
        print("Location: ", self.location)
        return self.location

    def compare_keywords_with_hobbies(self, keywords):
        with open('hobbies.csv', 'r') as csvFile:
            # with open('hobbies.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            for row in csv_reader:
                self.database_word_list_hobbies.append(row[0].lower())
            for word in keywords:
                for element in self.database_word_list_hobbies:
                    #if element in word:
                    if element == word:
                        #if word not in self.hobbies:
                        self.hobbies.append(element)
        #print("Hobbies: ", self.hobbies)
        #most_often_hobby = self.get_most_frequencies(self.hobbies)
        if self.hobbies:
            return self.hobbies
        return -1

    def get_most_frequencies(self,list):
        #print("HOBBY-LIST:",list)
        if list:
            if len(list)>=2:
                print("IN IF",list)
                counter = 0
                element_with_most_frequency = ""
                for i in list:
                    current_frequency = list.count(i)
                    if (current_frequency > counter):
                        counter = current_frequency
                        element_with_most_frequency = i
                return element_with_most_frequency
            else:
                return list[0]
        else:
            return -1

    def compare_keywords_with_occupations(self, keywords):
        with open('occupation.csv', 'r') as csvFile:
            # with open('hobbies.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            for row in csv_reader:
                self.database_word_list_occupation.append(row[0].lower())
            for word in keywords:
                for element in self.database_word_list_occupation:
                    #if element in word:
                    if element == word:
                        #if word not in self.occupation:
                        self.occupation.append(element)
        #most_often_occupation = self.get_most_frequencies(self.occupation)
        #print("Occupation: ", self.occupation)
        #print("mostoftenoccupation:", most_often_occupation)
        #return most_often_occupation
        if self.occupation:
            return self.occupation
        else:
            return -1

    """def compare_keywords_with_institutions(self, keywords):
        with open('institutions.csv', 'r') as csvFile:
            # with open('hobbies.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            for row in csv_reader:
                self.database_word_list_institutions.append(row[0].lower())
            for word in keywords:
                for element in self.database_word_list_institutions:
                    #if element in word:

                    if element == word:
                        print("ELEMENNNT",element)
                        #if word not in self.university:
                        self.institution.append(element)
        if self.institution:
            return self.institution
        else:
            return -1
    """
    def compare_keywords_with_institutions(self, html_string):
        text = str(html_string).lower()
        with open('institutions.csv', 'r') as csvFile:
            # with open('hobbies.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            for row in csv_reader:
                self.database_word_list_institutions.append(row[0].lower())
            for element in self.database_word_list_institutions:
                    #if element in word:
                if element in text:
                    print("ELEMENNNT",element)
                    #if word not in self.university:
                    self.institution.append(element)
        if self.institution:
            return self.institution
        else:
            return -1
    def compare_keywords_with_clubs(self,keywords):
        # TODO Vereinskürzel hinzufügen
        print("compare_keywords_with_clubs")

    def compare_email_with_name(self, firstname, secondname, mail):
        formatted_name = firstname.lower()+secondname.lower()
        local_part_of_mailaddress = mail.split("@")[0].lower()
        percentage_limit = 0.4
        if SequenceMatcher(None, formatted_name, local_part_of_mailaddress).ratio()>= percentage_limit:
            formatted_mail = mail.replace("(at)","@")
            self.emails.append(formatted_mail)

    def get_email(self, html_string, firstname, secondname):
        email_words = self.whitespace_wt.tokenize(html_string.lower())
        for fragment in email_words:
            mail_regex = re.search('(.*((@)|(\(at\))).*\.(de|com|net)).*', fragment)
            if mail_regex:
                print("Email found:",mail_regex.group(1))
                self.compare_email_with_name(firstname, secondname, mail_regex.group(1))
        print("Correct Emails: ", self.emails)
        if self.emails:
            return self.emails
        else:
            return -1

    def get_years(self, keywords):
        regex_string = "(geburtsdatum)|(alter)|(geboren)|(geburtsort)|(geburtstag)|(born)|(birth)"
        all_years_in_text = []
        year_lenth = 4
        for element in keywords:
            if re.match(r"[0-9]{4}", element) and len(element) == year_lenth:
                if 1900 <= int(element) <= 2019 and not element in all_years_in_text:
                    all_years_in_text.append(element)

        if all_years_in_text:
            print(all_years_in_text)
            for year in all_years_in_text:
                vistited_elements = 0
                max_number_of_visited_elements = 15
                #  to get all occurances of this year
                occurrences = [i for i, x in enumerate(keywords) if x == year]
                for position_of_year in occurrences:
                    while (position_of_year+vistited_elements) < len(
                            keywords)-1 and vistited_elements <= max_number_of_visited_elements and position_of_year is not -1:
                        index_behind = position_of_year+ vistited_elements
                        index_front = position_of_year - vistited_elements
                        if re.match(r""+regex_string, keywords[index_behind]):
                            print("Behind: Geburtsjahr wurde gefunden", year)
                            return year
                        elif re.match(r""+regex_string, keywords[index_front]):
                            print("Front: Geburtsjahr wurde gefunden", year)
                            return year
                        vistited_elements += 1
        return -1
        #print("Year of Webpage: ",average_year)
        #return average_year
