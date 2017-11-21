from operator import itemgetter
import requests, json, sys
import csv
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from stop_words import get_stop_words
from nltk.stem.snowball import SnowballStemmer

def readCSV(file = None):
    dataset = []
    with open(file,'r') as ins:
        datalist = ins.read().splitlines()

        for i in range(len(datalist)):
            line = datalist[i]
            list = line.split(';')
            dataset.append(list)
    
    return dataset

stop_words = get_stop_words('english')
stopWords = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")

stop_words.append(",")
stop_words.append(".")
stop_words.append("+")



dataset = readCSV('articles/articles.csv')

for x in range(1,len(dataset)):
    filteredWord = []
    filename = "articles_{0}".format(x)
    article = dataset[x][2]

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
    files = open("result/"+filename+'-result.json', 'w')
    files.write(result)
    files.close()

    routes = {}
    routes['title'] = dataset[x][1]
    routes['date'] = dataset[x][5]
    routes['url'] = dataset[x][9]

    with open('routes/routes.json', 'r') as f:
        datastore = json.load(f)
    datastore[filename] = routes

    datastore = json.dumps(datastore)
    files = open('routes/routes.json','w')
    files.write(datastore)
    files.close()

    with open('routes/keylist.json', 'r') as f:
        keylist = json.load(f)
    keylist["keylist"].append(filename)

    keylist = json.dumps(keylist)
    files = open('routes/keylist.json','w')
    files.write(keylist)
    files.close()
