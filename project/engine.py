from operator import itemgetter
import requests, json, sys, os
import csv
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from stop_words import get_stop_words
from nltk.stem.snowball import SnowballStemmer

from project import app

def readIndexing():
    filename = os.path.join(app.static_folder, 'routes/keylist.json')
    with open(filename, 'r') as f:
        data = json.load(f)

    return data['keylist']

def readResult(files):
    filename = os.path.join(app.static_folder, "result/"+files+"-result.json")
    with open(filename,'r') as f:
        data = json.load(f)
    
    return data

def readRoutes():
    filename = os.path.join(app.static_folder, "routes/routes.json")
    with open(filename,'r') as f:
        data = json.load(f)
    return data

def search(query):
    stop_words = get_stop_words('english')
    stopWords = set(stopwords.words('english'))
    stemmer = SnowballStemmer("english")

    stop_words.append(",")
    stop_words.append(".")
    stop_words.append("+")

    filteredWord = []
    tokenizing = word_tokenize(query)

    for word in tokenizing:
        if word not in stopWords and word not in stop_words:
            filteredWord.append(word)
    
    stemmingWord = []

    for word in filteredWord:
        stemmingWord.append(stemmer.stem(word))
    
    queryArr = []

    for word in stemmingWord:
        if word not in queryArr:
            queryArr.append(word)
    
    listArticle = readIndexing()
    queryResult = []

    for x in range(0,len(listArticle)):
        filename = listArticle[x]
        result = readResult(filename)
        tmp_score = 0
        for y in range(0,len(queryArr)):
            if queryArr[y] in result["index"]:
                tmp_score += result["counter"][result["index"][queryArr[y]]][1]
        
        if [filename,tmp_score] not in queryResult:
            queryResult.append([filename,tmp_score])
    
    queryResult.sort(key=itemgetter(1),reverse=True)

    result = []
    routes = readRoutes()
    for x in range(0,len(queryResult)):
        result.append(routes[queryResult[x][0]])
    return result
