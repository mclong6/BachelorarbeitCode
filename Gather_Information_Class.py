import csv
from nltk import WhitespaceTokenizer
import re
from difflib import SequenceMatcher
import datetime
import numpy

class GatherInformation:

    def __init__(self):
        self.database_word_list_hobbies = []
        self.database_word_list_location = []
        self.database_word_list_occupation = []
        self.database_word_list_universities = []
        self.location = []
        self.hobbies = []
        self.occupation = []
        self.university = []
        self.whitespace_wt = WhitespaceTokenizer()
        self.emails = []

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
                        if word not in self.location:
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
                        if word not in self.hobbies:
                            self.hobbies.append(element)
        print("Hobbies: ", self.hobbies)
        return self.hobbies

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
                        if word not in self.occupation:
                            self.occupation.append(element)
        print("Occupation: ", self.occupation)
        return self.occupation

    def compare_keywords_with_universities(self, keywords):
        with open('universities.csv', 'r') as csvFile:
            # with open('hobbies.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            for row in csv_reader:
                self.database_word_list_universities.append(row[0].lower())
            for word in keywords:
                for element in self.database_word_list_universities:
                    #if element in word:
                    if element == word:
                        if word not in self.university:
                            self.university.append(element)
        print("Universities: ",self.university)
        return self.university

    def compare_keywords_with_clubs(self,keywords):
        # TODO Vereinskürzel hinzufügen


        """with open("person_information.csv", "a") as file:
            fieldnames = ["firstname", "secondname", "location", "year_of_birth", "estimated_year_of_birth",
                          "institution", "email", "hobbies", "occupation", "universities"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            # writer.writeheader()
            if self.hobbies is not "":
                writer.writerow({"hobbies": self.hobbies})"""

    def compare_email_with_name(self, firstname, secondname, mail):
        formatted_name = firstname.lower()+secondname.lower()
        local_part_of_mailaddress = mail.split("@")[0]
        percentage_limit = 0.4
        if SequenceMatcher(None, formatted_name, local_part_of_mailaddress).ratio()>= percentage_limit:
            self.emails.append(mail)

    def get_email(self, html_string, firstname, secondname):
        email_words = self.whitespace_wt.tokenize(html_string.lower())
        for element in email_words:
            # element = "lang@pw-metallbau.de"
            if re.match(r".*@.*\.(de|com|net)", element) is not None:
                print("Email found:" + element)
                self.compare_email_with_name(firstname, secondname, element)

                """with open("person_information.csv", "a") as file:
                    fieldnames = ["firstname", "secondname", "location", "year_of_birth", "estimated_year_of_birth",
                                  "institution", "email", "hobbies", "occupation"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    # writer.writeheader()
                    writer.writerow(
                        {"email": element})"""
        print("Correct Emails: ", self.emails)
        return self.emails

    def get_years(self, html_string):
        #print(html_string)
        average_year = -1
        date = datetime.datetime.now()
        number_of_characters=0
        max_number_of_characters=100
        min_year = 1700
        all_years_in_text = []
        correct_years_in_text = []
        string_behind_copyright= ""
        position = html_string.find("©")
        print("position:",position,"length: ",len(html_string))
        while position < len(html_string)and number_of_characters <= max_number_of_characters and position is not -1:
            print(html_string[position])
            string_behind_copyright += (html_string[position])
            position += 1
            number_of_characters += 1
        years_behind_copyright = re.findall(r"[0-9]{4}",string_behind_copyright)

        if years_behind_copyright:
            int_years_behind_copyright = list(map(int, years_behind_copyright))
            average_year = numpy.mean(int_years_behind_copyright)
            average_year = int(round(average_year))
            print("Year behind Copyright: ", average_year)
        else:
            all_years_in_text = re.findall(r"[0-9]{4}", html_string)
            average_year = -1
            if all_years_in_text:
                for element in all_years_in_text:
                    if not int(element) < min_year and not int(element) > int(date.year):
                        correct_years_in_text.append(int(element))
                average_year = numpy.mean(correct_years_in_text)
                average_year = int(round(average_year))

        print(average_year)
        return average_year
