'''
author = Robert Horváth
'''


#Declare base variables
separator = "----------------------------------------"
users = {"bob":"123","ann":"pass123","mike":"password123","liz":"pass123"}

TEXTS = ['''
Situated about 10 miles west of Kemmerer, 
Fossil Butte is a ruggedly impressive 
topographic feature that rises sharply 
some 1000 feet above Twin Creek Valley 
to an elevation of more than 7500 feet 
above sea level. The butte is located just 
north of US 30N and the Union Pacific Railroad, 
which traverse the valley. .''',

'''At the base of Fossil Butte are the bright 
red, purple, yellow and gray beds of the Wasatch 
Formation. Eroded portions of these horizontal 
beds slope gradually upward from the valley floor 
and steepen abruptly. Overlying them and extending 
to the top of the butte are the much steeper 
buff-to-white beds of the Green River Formation, 
which are about 300 feet thick.''',

'''The monument contains 8198 acres and protects 
a portion of the largest deposit of freshwater fish 
fossils in the world. The richest fossil fish deposits 
are found in multiple limestone layers, which lie some 
100 feet below the top of the butte. The fossils 
represent several varieties of perch, as well as 
other freshwater genera and herring similar to those 
in modern oceans. Other fish such as paddlefish, 
garpike and stingray are also present.'''
]


#Get username and password
username = input("Username:")
password = input("Password:")

#Check given credentials
if users.get(username) != password:
    print(separator)
    print("Wrong username or password!")
    print("Closing...")
    print(separator)
    exit()

#If all OK proceed
print("Welcome to the app, " + username)
print(f"We have {len(TEXTS)} texts to be analyzed.")
print(separator)

#Get users input & verify if OK - otherwise exit
selection = input(f"Enter number btw. 1 and {len(TEXTS)} to select:")
print(separator)

if selection.isdigit() and not int(selection) > len(TEXTS) and not int(selection) == 0:
    #OK -> change type to int
    selection = int(selection)
else:
    print("Wrong selection!")
    print("Closing...")
    print(separator)
    exit()

#Get the selected text from TEXTS and split it into separate strings
split_selected = TEXTS[(selection)-1].strip().split()

#Delete unwanted symbols
unwanted_chars = ".,'!?&#^|-@();€$:<>+-%´ˇ[]/¨" + '"'

for index in range(len(split_selected)):
    for char in unwanted_chars:
        split_selected[index] = split_selected[index].replace(char,"")

#Get rid of all None strings
split_selected = list(filter(None, split_selected))

#Create dictionary with keys based on longest word length 
occurencies = dict.fromkeys(range(1,len(max(split_selected, key=len))+1),0)

#Declare and get sum values from selected text 
#And their occurency sums
words_count = len(split_selected)
title_count = 0
upper_count = 0
lower_count = 0
numeric_count = 0
numeric_sum = 0

for word in split_selected:
    if word.istitle():
        title_count += 1
    elif word.isupper():
        upper_count += 1
    elif word.islower():
        lower_count += 1
    elif word.isnumeric():
        numeric_count += 1
        numeric_sum += int(word)
    #Get words occurencies sums
    length_index = len(word)
    occurencies[length_index] = occurencies[length_index] + 1 
    
#Print values 
print("There are",words_count,"words in the selected text.")
print("There are",title_count,"titlecase words.")
print("There are",upper_count,"uppercase words.")
print("There are",lower_count,"lowercase words.")
print("There are",numeric_count,"numeric strings.")
print("The sum of all the numbers:",numeric_sum)


#Visualization of word length occurencies section

#Declare variables for graph
graph_header_start = "LEN"
graph_header_middle = "OCCURENCES"
graph_header_end = "NR."
graph_start_count = len("LEN")
graph_middle_count = len(graph_header_middle)

#Adjust the middle part of graph header accordingly to the longest sum of occurencies
max_occurencies = max(occurencies.values())

if graph_middle_count < max_occurencies:
    #+2 for additional spaces
    count = max_occurencies - graph_middle_count + 2
    if not count % 2 == 0:
        count += 1
    graph_header_middle = f"{ ' ' * int(count/2) }OCCURENCES{ ' ' * int(count/2) }"
    graph_middle_count = len(graph_header_middle)

#Print graph header
print(separator)
print(graph_header_start,graph_header_middle, graph_header_end, sep="|")
print(separator)

    
#Print occurencis as graph
for key, value in occurencies.items():
    start_space = graph_start_count - len(str(key))
    middle_space = graph_middle_count - value
    print(f"{ ' ' * start_space }{key}|{ '*' * value }{ ' ' * middle_space }|{value}")

#END
print(separator)