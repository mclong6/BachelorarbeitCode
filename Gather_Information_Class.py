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
        self.database_word_list_universities = []
        self.location = []
        self.hobbies = []
        self.occupation = []
        self.university = []
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
        print("Hobbies: ", self.hobbies)
        test = self.get_most_frequencies(self.hobbies)

        return test

    def get_most_frequencies(self,list):
        print("HOBBY-LIST:",list)
        if list:
            counter = 0
            element_with_most_frequency = ""
            for i in list:
                current_frequency = list.count(i)
                if (current_frequency > counter):
                    counter = current_frequency
                    element_with_most_frequency = i
            return element_with_most_frequency
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
        print("compare_keywords_with_clubs")

    def compare_email_with_name(self, firstname, secondname, mail):
        formatted_name = firstname.lower()+secondname.lower()
        local_part_of_mailaddress = mail.split("@")[0].lower()
        percentage_limit = 0.4
        if SequenceMatcher(None, formatted_name, local_part_of_mailaddress).ratio()>= percentage_limit:
            self.emails.append(mail)

    def get_email(self, html_string, firstname, secondname):
        email_words = self.whitespace_wt.tokenize(html_string.lower())
        pattern = re.compile(r".*((@)|(\(at\))).*\.(de|com|net)")
        for element in email_words:
            mail_regex = re.search('(.*((@)|(\(at\))).*\.(de|com|net)).*', element)
            if mail_regex:
                print("Email found:",mail_regex.group(1))
                self.compare_email_with_name(firstname, secondname, mail_regex.group(1))
          # element = "lang@pw-metallbau.de"
            #if re.match(r".*((@)|(\(at\))).*\.(de|com|net).*", element) is not None:
                #print("Email found:" + element)
                #self.compare_email_with_name(firstname, secondname, element)

        print("Correct Emails: ", self.emails)
        return self.emails

    def get_years(self, keywords):
        date = datetime.datetime.now()
        regex_string = "(geburtsdatum)|(alter)|(geboren)|(geburtsort)|(geburtstag)|(born)|(birth)"
        all_years_in_text = []
        for element in keywords:
            if re.match(r"[0-9]{4}", element) and len(element)==4:
                if 1900 <= int(element) <= 2019 and not element in all_years_in_text:
                    all_years_in_text.append(element)
        if all_years_in_text:
            print(all_years_in_text)
            for year in all_years_in_text:
                vistited_elements = 0
                max_number_of_visited_elements = 20
                #to get all occurances of this year
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

        """  while position < len(html_string)and vistited_elements <= max_number_of_visited_elements and position is not -1:
            average_year = -1
            
                    

                    #print(string_behind_year.replace("\n"," "))
                    #print(string_in_front_year)


            string_behind_copyright += (html_string[position])
            position += 1
            vistited_elements += 1
        years_behind_copyright = re.findall(r"[0-9]{4}",string_behind_copyright)

        if years_behind_copyright:
            int_years_behind_copyright = list(map(int, years_behind_copyright))
            average_year = numpy.mean(int_years_behind_copyright)
            average_year = int(round(average_year))
        else:
            all_years_in_text = re.findall(r"[0-9]{4}", html_string)
            average_year = -1
            if all_years_in_text:
                for element in all_years_in_text:
                    if not int(element) < min_year and not int(element) > int(date.year):
                        correct_years_in_text.append(int(element))
                average_year = numpy.mean(correct_years_in_text)
                average_year = int(round(average_year))
                max_number_of_visited_elements = 70
                for year in all_years_in_text:
                    counter = 0
                    position_of_year = html_string.find(year)
                    string_behind_year = ""
                    while position_of_year < len(html_string) and counter <= max_number_of_visited_elements and position_of_year is not -1:
                        string_behind_year+= (html_string[position_of_year])
                        position_of_year += 1
                        counter += 1
        """
        #print("Year of Webpage: ",average_year)
        #return average_year
