from operator import itemgetter
import requests, json, sys,os
import csv
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from stop_words import get_stop_words
from nltk.stem.snowball import SnowballStemmer

from project import app

stop_words = get_stop_words('english')
stopWords = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")

stop_words.append(",")
stop_words.append(".")
stop_words.append("+")



def generate(data):
    filepath = os.path.join(app.static_folder, "routes/routes.json")
    with open(filepath,'r') as f:
        length = len(json.load(f)) +1
    
    print length
    valid = False
    filteredWord = []
    filename = "articles_{0}".format(length)
    article = data['article']
    tokenizing = word_tokenize(article)

    for word in tokenizing:
        if word not in stopWords and word not in stop_words:
            filteredWord.append(word)

    stemmingWord = []

    for word in filteredWord:
        stemmingWord.append(stemmer.stem(word))

    objectData = {}
    counterData = []

    for word in stemmingWord:
        if word not in counterData:
            counterData.append(word)
            objectData[word] = 1
        else:
            objectData[word] += 1

    temp = []

    for w in counterData:
        temp.append([w,objectData[w]])

    temp.sort(key=itemgetter(1),reverse=True)

    for w in range(0,len(temp)):
        objectData[temp[w][0]] = w

    result = {}
    result['index'] = objectData
    result['counter']= temp

    result = json.dumps(result)
    filepath = os.path.join(app.static_folder, "result/"+filename+"-result.json")
    files = open(filepath, 'w')
    files.write(result)
    files.close()

    routes = {}
    routes['title'] = data['title']
    routes['date'] = data['date']
    routes['url'] = data['url']

    filepath = os.path.join(app.static_folder, "routes/routes.json")
    with open(filepath, 'r') as f:
        datastore = json.load(f)
    datastore[filename] = routes

    datastore = json.dumps(datastore)
    filepath = os.path.join(app.static_folder, "routes/routes.json")
    files = open(filepath,'w')
    files.write(datastore)
    files.close()

    filepath = os.path.join(app.static_folder, "routes/keylist.json")
    with open(filepath, 'r') as f:
        keylist = json.load(f)
    
    if filename not in keylist:
        keylist["keylist"].append(filename)

    keylist = json.dumps(keylist)
    filepath = os.path.join(app.static_folder, "routes/keylist.json")
    files = open(filepath,'w')
    files.write(keylist)
    files.close()
    valid = True

    return valid
