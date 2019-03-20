import csv

player_information_list = []
no_birth_date = '()'
def get_player_information_from_csvfile():
    with open('linksToPlayerFile.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        included_cols = [0,1, 2, 5]
        for row in reader:
            content = list(row[i] for i in included_cols)
            player_information_list.append(content)
        #print(player_information_list)
        for element in player_information_list:
            create_mail(element)
    csvFile.close()
def formate_birth_date(birth_date):
    formatted_birth_date = birth_date.split()[0]
    if formatted_birth_date == no_birth_date:
        year_of_birth = no_birth_date
    else:
        year_of_birth = formatted_birth_date.split(".")[2]
    return year_of_birth

def create_mail(player_information):
    first_name = player_information[0]
    second_name = player_information[1]
    last_name = player_information[2]
    year_of_birth = formate_birth_date(player_information[3])

    print(first_name, second_name, last_name, year_of_birth)


S = {'firstname', 'secondname', '1995'}

collect = set()
step = {''}
while step:
    '''for a in step:
        for b in S:
            if len(a+b)<=24:
                if not a==b:
                    step.add(a+b)
'''
    # step = set(a+b for a in step for b in S if len(a+b) <= 24)
    step = set(a+b for a in step for b in S if len(a+b)<=24 and not b in a)

    collect |= step

print(sorted(collect))

#get_player_information_from_csvfile()