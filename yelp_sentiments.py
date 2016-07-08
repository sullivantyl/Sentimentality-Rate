"""
This python program takes the information provided by a json file and extracts / filters the words from
the yelp reviews included, then weighs the value of each word per review by the star value of the
associated review, determining its "sentiment" and sorts the list into the top 500 and
bottom 500 weighed words.

By: Tyler Sullivan

"""

import nltk
import json
import csv
import time

# gathers data from json file of yelp reviews
try:
    with open("yelp_academic_dataset_review_small.json") as infile:
        data = json.load(infile)
        infile.close()
except:
    print("Error reading JSON file")

# nltk tools to be shortened and used
try:
    swords = set(nltk.corpus.stopwords.words(fileids = "english"))
    words = set(nltk.corpus.words.words())
    names = set([name.lower() for name in nltk.corpus.names.words()])
    lem = nltk.stem.WordNetLemmatizer()
except:
    print("Error getting nltk modules")

# some declarations to increase stability
data_list = []
weighted_list = [{'word' : '', 'stars' : [], 'count': 0, 'weight' : 0.0}]

# data size limiter for testing purposes
tlength = len(data)
# comment out following line for full run, or use as slicer for testing
# data = data[:1000]
total = len(data)

print('{: <20s} {:>10d}'.format("Total Items:", len(data)))
print('{: <20s} {:>10d} {:>15.2f}%'.format("Operation Items:", len(data), (len(data) / tlength * 100)) + ' of total\n')

# set clock
count = 0
t0 = time.clock()

# parse rating and review from data gathered from json file
for item in data:
    count = count + 1
    percent = count / total
    print('{:<20s} {:>10.2f}% {:15.2f}s'.format("\rMaking list...", percent*100, time.clock() - t0), end='')
    data_list.append([item["stars"], item["text"].lower()])

# reset clock and output
print('')
count = 0
t0 = time.clock()

# filter words in the review and format for future operations
for element in data_list:
    count = count + 1
    percent = count / total
    print('{:<20s} {:>10.2f}% {:15.2f}s'.format("\rFiltering words...", percent*100, time.clock() - t0), end='')
    # this portion weighs once per review                   #   alternatively for weighing with significance for multiples
    element[1] = set(nltk.word_tokenize(element[1]))        #   element[1] = nltk.word_tokenize(element[1])
    element[1] -= swords                                    #   element[1] = [word for word if word not in swords]
    element[1] -= names                                     #   element[1] = [word for word if word not in names]
    element[1] &= words                                     #   element[1] = [word for word if word in words]

# reset clock and output
print('')
count = 0
t0 = time.clock()

# creates dictionary entries for words in reviews with weights
for [stars, reviews] in data_list:
    count = count + 1
    percent = count / total
    print('{:<20s} {:>10.2f}% {:15.2f}s'.format("\rWeighing words...", percent*100, time.clock() - t0), end='')
    for word in reviews:
        lword = lem.lemmatize(word)
        check = False
        for ww in weighted_list:
            if (ww['word'] == lword):
                ww['stars'].append(stars)
                ww['count'] += 1
                ww['weight'] = sum(ww['stars']) / ww['count']
                check = True
                break
        if not check:
            weighted_list.append({'word' : lword, 'stars' : [stars], 'count' : 1, 'weight' : stars})
print('')

# removes irrelevent words
weighted_list = [ww for ww in weighted_list if ww['count'] >= 10]

# sorts and splits dictionary of words
weighted_list.sort(key = lambda w: w['weight'])
bottom500 = weighted_list[:500]
weighted_list.reverse()
top500 = weighted_list[:500]

# exports data to formatted csv file
try:
    with open("output.csv", "w") as outfile:
        w = csv.writer(outfile)
        w.writerow(["Positive Word", "Weight", "", "Negative Word", "Weight"])
        for i in range (0, len(top500)):
            w.writerow([top500[i]['word'], "{:.2f}".format(top500[i]['weight']), '', bottom500[i]['word'], "{:.2f}".format(bottom500[i]['weight'])])
        outfile.close()
except:
    print("Error with CSV operations")
