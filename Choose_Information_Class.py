import numpy
from collections import Counter


# This class selects the information that most closely matches the person.
class ChooseInformation:
    def __init__(self):
        self.key_institution = 1
        self.key_other = 2

    # choose an element from a list with the highest score, score will be calculated
    def get_highest_score(self, list_with_scores, key):
        if key == self.key_other:
            for i in range(0, len(list_with_scores)):
                list_with_scores[i].sort(key=Counter(list_with_scores[i]).get, reverse=True)
        instances = []      # instances correspond to the columns in the matrix
        if list_with_scores:
            # get all instances
            for i in range(0, len(list_with_scores)):
                for k in range(0, len(list_with_scores[i])):
                    if list_with_scores[i][k] not in instances:
                        instances.append(list_with_scores[i][k])
            # because shorter institution_names could be inside another name
            if key == self.key_institution:
                instances.sort(key=len, reverse=True)
                print("instances", instances)
            # create list3 with scores
            list3 = []
            for i in range(0, len(list_with_scores)):
                list2 = []
                if list_with_scores[i]:
                    for k in range(0, len(list_with_scores[i])):
                        list1 = []
                        frequency = list_with_scores[i].count(list_with_scores[i][k])
                        score = frequency / len(list_with_scores[i])
                        list1.append(list_with_scores[i][k])
                        list1.append(score)
                        if len(list2) == 0:
                            list2.append(list1)
                        else:
                            in_list = True
                            for l in range(0, len(list2)):
                                if list1[0] in list2[l][0]:
                                    in_list = False
                            if in_list:
                                list2.append(list1)
                    list3.append(list2)
            print("Liste mit Scores: ", list3)

            # create matrix with numpy
            matrix = numpy.zeros(shape=(len(list3),len(instances)))
            # fill matrix
            for i in range(0,len(list3)):
                for k in range(0,len(list3[i])):
                    index = instances.index(list3[i][k][0])
                    matrix[i][index] = (list3[i][k][1])
            print(matrix)

            score = 0
            element_with_highest_score = ""
            # every column
            for k in range(0, numpy.size(matrix, 1)):
                # current_score = sum of elements of a column
                current_score = 0
                # every row
                for i in range(0,numpy.size(matrix,0)):
                    current_score = current_score + matrix[i][k]
                current_score = current_score / len(list3)
                if current_score > score:
                    score = current_score
                    element_with_highest_score = instances[k]
            print("Element mit dem höchsten Score: ", element_with_highest_score, " Score: ", score)
            return element_with_highest_score
