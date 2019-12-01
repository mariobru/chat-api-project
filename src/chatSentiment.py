#!/usr/bin/python3
import requests
from textblob import TextBlob

def chatSent(idchat):
    id_chat = str(idchat)
    URL = 'http://localhost:8080/chat/{}/list'.format(id_chat)
    messages = requests.get(URL).json()
    print(messages)
    polarity = 0
    subjectivity = 0
    for e in messages:
        polarity += TextBlob(*e).sentiment[0]
        subjectivity += TextBlob(*e).sentiment[1]
    polarity_mean = polarity/len(messages)
    subjectivity_mean = subjectivity/len(messages)
    return {'Polarity mean': polarity_mean, 'Subjectivity mean': subjectivity_mean}