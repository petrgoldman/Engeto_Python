'''
author = Petr Goldman
'''
TEXTS = ['''
Situated about 10 miles west of Kemmerer, 
Fossil Butte is a ruggedly impressive 
topographic feature that rises sharply 
some 1000 feet above Twin Creek Valley 
to an elevation of more than 7500 feet 
above sea level. The butte is located just 
north of US 30N and the Union Pacific Railroad, 
which traverse the valley. ''',

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

delimiter = '-'*40
print(delimiter)
print('Welcome to the app. Please log in: ')

logins = {'bob': '123', 'ann': 'pass123', 'mike': 'password123', 'liz': 'pass123'}
username = input('USERNAME: ')
password = input('PASSWORD: ')

while (username not in logins.keys()) or (logins.get(username,'') != password):
    print('Mas spatnou pamet, zkus to znova!')
    username = input('USERNAME: ')
    password = input('PASSWORD: ')
print('Login successful!')
print(delimiter)

text_num = 0
while text_num < 1 or text_num > 3:
    text_num = int(input('Enter a number btw. 1 and 3 to select: '))
print(delimiter)

text = TEXTS[text_num - 1].lstrip('\n').rstrip(' ')
words = text.replace(',', '').replace('.', '').replace('\n', '').split(' ')

num_of_words = 0
title_words = 0
upper_words = 0
lower_words = 0
numeric_words = 0
sum_of_num_words = 0
bar_chart = dict()

while words:
    word = words.pop()
    num_of_words += 1
    if word.istitle():
        title_words += 1
    if word.isupper():
        upper_words += 1
    if word.islower():
        lower_words += 1
    if word.isdigit():
        numeric_words += 1
        sum_of_num_words += int(word)
    word_len = len(word)
    if word_len in bar_chart.keys():
        bar_chart[word_len] += 1
    else:
        bar_chart[word_len] = 1

print(f'There are {num_of_words} words in the selected text.')
print(f'There are {title_words} titlecase words')
print(f'There are {upper_words} uppercase words')
print(f'There are {lower_words} lowercase words')
print(f'There are {numeric_words} numeric strings')
print(delimiter)

bar_items = sorted(bar_chart.items())
for item in bar_items:
    print(str(item[0]) + ' ' + '*'*item[1] + ' ' + str(item[1]))

print(delimiter)
print(f'If we summed all the numbers in this text we would get: {sum_of_num_words}')
print(delimiter)